"""Generate Conversations Turn 2"""
import os
import json
import fire
import torch
import hydra
import random
import logging
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *
from helpers import get_formatted_responses

logging.basicConfig(level=logging.INFO)


@hydra.main(version_base=None, config_path="config", config_name="conversations_turn_2")
def main(args: DictConfig) -> None:
    logging.info(f"""Generating Conversations Turn 2. 
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
    
    # only keep up to max users used during training
    users = {
        k: v for k, v in users.items() 
        if int(k.split("_")[1]) < args.n_users
    }
    
    # eig turn 1
    with open(args.eig_turn_1, "r") as f:
        eig_turn_1 = json.load(f)
        
    # keep track of turn 1 vars
    turn_1_vars = {
        "question_turn_1": [],
        "answer_turn_1": [],
        "users": [],
    }
    
    # prompt questioner
    batch_prompts_questioner = []
    
    for i in range(args.prompt_start, args.prompt_end):
        
        prompt = prompts[i]
        
        eig_key = f"best_question_for_prompt_{i}"
    
        question_turn_1 = eig_turn_1[eig_key]["best_question"]
        answers_turn_1 = eig_turn_1[eig_key]["responses"]
        users_turn_1 = eig_turn_1[eig_key]["user"]
        
        turn_1_vars["question_turn_1"].append(question_turn_1)
        turn_1_vars["answer_turn_1"].append(answers_turn_1)
        turn_1_vars["users"].append(users_turn_1)
        
        for answer in answers_turn_1:
            
            formatted_prompt = QUESTION_PROMPT_TURN_2.format(
                prompt=prompt, 
                clarifying_question=question_turn_1,
                response=answer,
            )
        
            batch_prompts_questioner.append([
                {"role": "user", "content": formatted_prompt}
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
    n_user = args.n_users_per_prompt
    question_counter = 0
    
    for i in range(args.prompt_start, args.prompt_end):
        
        prompt = prompts[i] 
        
        question_turn_1 = turn_1_vars["question_turn_1"][i]
        answers_turn_1 = turn_1_vars["answer_turn_1"][i]
        rand_users = turn_1_vars["users"][i]
       
        max_words = 10
            
        for j, rand_user_id in enumerate(rand_users):
            
            user = users[f"user_{rand_user_id}"]
            rand_user_ids.append(rand_user_id)
            answer = answers_turn_1[j]
            
            for question_attempt in range(n):
            
                batch_prompts_roleplayer.append([
                        {"role": "system", "content": f"You are roleplaying the following persona: {user}"},
                        {"role": "assistant", "content": prompt},
                        {"role": "user", "content": f"{question_turn_1}"},
                        {"role": "assistant", "content": answer},
                        {"role": "user", "content": f"{formatted_batch_responses_questioner[question_counter]}\n\nRespond in no more than {max_words} words."},
                        {"role": "assistant", "content": ""},
                    ])
                question_counter += 1
            
    formatted_batch_responses_roleplayer = get_formatted_responses(
        model=model,
        tokenizer=tokenizer,
        prompts=batch_prompts_roleplayer,
        config=args.generation_config_roleplayer,
        output_format="Roleplayer",
        invalid_output="<|invalid_response|>",
    )
 
    # formatting
    conversations = {
        "id": [],
        "user_id": [],
        "prompt": [],
        "attempt": [],
        "question_turn_1": [],
        "response_turn_1": [],
        "question_turn_2": [],
        "response_turn_2": [],
    }
    
    response_idx = 0
    
    for i in range(args.prompt_start, args.prompt_end): # for all prompts 
        prompt = prompts[i]
        
        question_turn_1 = turn_1_vars["question_turn_1"][i]
        answers_turn_1 = turn_1_vars["answer_turn_1"][i]
        rand_users = turn_1_vars["users"][i]
        
        for j, user_id in enumerate(rand_users):
            
            for question_attempt in range(n):

                try:
                    conversations["id"].append(i)
                    conversations["user_id"].append(user_id)
                    conversations["prompt"].append(prompt)
                    conversations["attempt"].append(question_attempt)
                    conversations["question_turn_1"].append(question_turn_1)
                    conversations["response_turn_1"].append(answers_turn_1[j])
                    
                    question_turn_2 = formatted_batch_responses_questioner[response_idx]
                    response_turn_2 = formatted_batch_responses_roleplayer[response_idx]
                    conversations["question_turn_2"].append(question_turn_2)
                    conversations["response_turn_2"].append(response_turn_2)
                except:
                    conversations["id"].append(i)
                    conversations["user_id"].append(user_id)
                    conversations["prompt"].append(prompt)
                    conversations["attempt"].append(question_attempt)
                    conversations["question_turn_1"].append("<|invalid_response|>")
                    conversations["response_turn_1"].append("<|invalid_response|>")
                    conversations["question_turn_2"].append("<|invalid_response|>")
                    conversations["response_turn_2"].append("<|invalid_response|>")

                response_idx += 1
    
    with open(args.save_file, "w") as f:
        json.dump(conversations, f, indent=4)
        

if __name__ == "__main__":
    fire.Fire(main())