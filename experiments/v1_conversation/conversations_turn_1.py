"""Generate Conversations Turn 1: q_i ~ model(q | x_i) and h_ij ~ model(h | x_i, q_i, u_j)"""
import os
import json
import fire
import torch
import hydra
import random
import logging
import numpy as np
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *
from helpers import get_formatted_responses

logging.basicConfig(level=logging.INFO)


@hydra.main(version_base=None, config_path="config", config_name="conversations_turn_1")
def main(args: DictConfig) -> None:
    logging.info(f"""Generating Conversations Turn 1. 
Start Prompt: {args.prompt_start}
End Prompt: {args.prompt_end}
Saving to: {args.save_file}
Seed: {args.seed}
N Users Per Prompt: {args.n_users_per_prompt}""")
    
    # seed
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)

    # model
    model = VLLMInferenceModel(
        **args.model_config
    )
    
    # tokenizer 
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=args.model_config.model,
        cache_dir=args.model_config.download_dir,
    )
    
    # prompts
    with open(args.prompts, "r") as f:
        prompts = json.load(f)
                
    # users
    with open(args.users, "r") as f:
        users = json.load(f)
    
    # only use users up to n_users
    users = {
        k: v for k, v in users.items() 
        if int(k.split("_")[1]) < args.n_users
    }
    
    # prompt questioner (independent of users)
    batch_prompts_questioner = []
    for i in range(args.prompt_start, args.prompt_end):
        
        prompt = prompts[i]
        
        batch_prompts_questioner.append([
            {"role": "user", "content": QUESTION_PROMPT.format(question=prompt)}
        ])
        
    formatted_batch_responses_questioner = get_formatted_responses(
        model=model,
        tokenizer=tokenizer,
        prompts=batch_prompts_questioner,
        config=args.generation_config_questioner,
        output_format="Clarifying Question:",
        invalid_output="<|invalid_response|>",
    )    
    
    # prompt roleplayer
    batch_prompts_roleplayer = []
    rand_user_ids = []
    n = args.generation_config_questioner.num_return_sequences 
    
    for i, question in enumerate(formatted_batch_responses_questioner):
        
        prompt = prompts[i//n] 
        
        if i % n == 0:
            if not args.selected_users:
                if i == 0:
                    logging.info(f"Randomly sample {args.n_users_per_prompt} from {args.n_users} users.")
                rand_users = torch.randperm(args.n_users)[:args.n_users_per_prompt].tolist()
            else:
                if i == 0:
                    logging.info(f"Sample from 1 user pair from {args.selected_users}")
                rand_idx = np.random.choice(np.arange(len(args.selected_users)), 1).item()
                rand_users = args.selected_users[rand_idx]
            
            max_words = torch.normal(mean=args.roleplayer_mean_words, std=args.roleplayer_std_words, size=(1,))
            max_words = torch.clamp(max_words, args.roleplayer_min_words, args.roleplayer_max_words).int().item()            
            
        for rand_user_id in rand_users:            
            user = users[f"user_{rand_user_id}"]
            rand_user_ids.append(rand_user_id)
            batch_prompts_roleplayer.append([
                    {"role": "system", "content": f"You are roleplaying the following persona: {user}"},
                    {"role": "assistant", "content": prompt},
                    # # Only for maximizing EIG and modifying gold responses
                    # {"role": "user", "content": f"{question}\n\nRespond in no more than 30 words."},                    
                    {"role": "user", "content": f"{question}\n\nRespond in no more than {max_words} words."},
                    {"role": "assistant", "content": ""},
            ]) 
    
    formatted_batch_responses_roleplayer = get_formatted_responses(
        model=model,
        tokenizer=tokenizer,
        prompts=batch_prompts_roleplayer,
        config=args.generation_config_roleplayer,
        output_format="Roleplayer",
        invalid_output="<|invalid_response|>",
    )
   
    # format data
    conversations = {
        "id": [],
        "user_id": [],
        "prompt": [],
        "attempt": [],
        "question": [],
        "response": [],
    }
    
    rand_user_idx = 0
    response_idx = 0
    
    for prompt_id in range(args.prompt_start, args.prompt_end): # for all prompts 
        for question_attempt in range(args.generation_config_questioner.num_return_sequences):
            for _ in range(args.n_users_per_prompt): # and we gave each attempt to a random sample of n users 
                try:
                    conversations["id"].append(prompt_id)
                    conversations["user_id"].append(rand_user_ids[rand_user_idx])
                    conversations["prompt"].append(prompts[prompt_id])
                    conversations["attempt"].append(question_attempt)
                    question = formatted_batch_responses_questioner[response_idx//args.n_users_per_prompt]
                    response = formatted_batch_responses_roleplayer[response_idx]
                    conversations["question"].append(question)
                    conversations["response"].append(response)
                except:
                    conversations["id"].append(prompt_id)
                    conversations["user_id"].append(rand_user_ids[rand_user_idx])
                    conversations["prompt"].append(prompts[prompt_id])
                    conversations["attempt"].append(question_attempt)
                    conversations["question"].append("<|invalid_response|>")
                    conversations["response"].append("<|invalid_response|>")
                rand_user_idx += 1
                response_idx += 1
    
    
    with open(args.save_file, "w") as f:
        json.dump(conversations, f, indent=4)
        

if __name__ == "__main__":
    fire.Fire(main())