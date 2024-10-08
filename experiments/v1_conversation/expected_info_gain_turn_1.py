"""Compute EIG Turn 1."""
import os
import json
import fire
import torch
import tqdm
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


@hydra.main(version_base=None, config_path="config", config_name="expected_info_gain_turn_1")
def main(args: DictConfig) -> None:
    logging.info(f"""Computing EIG.
Saving to: {args.save_file}
N Users Per Prompt: {args.n_users_per_prompt}""")

    # model
    model = VLLMInferenceModel(
        **args.model_config
    )
    
    # tokenizer 
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=args.model_config.model,
        cache_dir=args.model_config.download_dir,
    )
    
    # gold responses
    with open(args.gold_responses, "r") as f:
        gold_responses = json.load(f)

    gold_responses = {
        f"{prompt_id}_{user_id}": gold_response for prompt_id, user_id, _, gold_response in
        zip(*gold_responses.values())
    }
        
    # conversations
    with open(args.conversations, "r") as f:
        conversations = json.load(f)
        
    conversation_dict = {}
    for prompt_id, user_id, prompt, attempt, question, response in zip(*conversations.values()):
        conversation_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
        conversation_dict[conversation_key] = {"prompt": prompt, "question": question, "response": response}
        
    # logprobs container
    logprobs = {}

    for prompt_id in tqdm.tqdm(set(conversations["id"])):
                
        for attempt in set(conversations["attempt"]):
            
            prompt_attempt_users = [
                int(key.split("_")[3])
                for key in conversation_dict.keys()
                if int(key.split("_")[1]) == prompt_id and 
                int(key.split("_")[-1]) == attempt
            ]            
            if args.users:
                user_list = args.users
            else:
                user_list = prompt_attempt_users
            
            for user_id in user_list:                        
                attempt_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
                logprobs[attempt_key] = []                

                # now to get the distributions of the above logprobs for each attempt_key, we need to compute logprobs across gold responses for each user 
                for other_user_id in prompt_attempt_users:                    
                    conversation_key = f"prompt_{prompt_id}_user_{other_user_id}_attempt_{attempt}"
                    gold_response_key = f"{prompt_id}_{user_id}"                    
                    conversation = conversation_dict[conversation_key]
                    gold_response = gold_responses[gold_response_key]                    

                    prompt_without_response = [
                        {"role": "user", "content": conversation["prompt"]},
                        {"role": "assistant", "content": conversation["question"]},
                        {"role": "user", "content": conversation["response"]},
                        {"role": "assistant", "content": ""},
                    ]
                    
                    prompt_with_response = [
                        {"role": "user", "content": conversation["prompt"]},
                        {"role": "assistant", "content": conversation["question"]},
                        {"role": "user", "content": conversation["response"]},
                        {"role": "assistant", "content": gold_response},
                    ]
                            
                    # format 
                    formatted_prompt_without_response = tokenizer.apply_chat_template(prompt_without_response, tokenize=True)[:-1] # :-1 to ignore eos token
                    formatted_prompt_with_response = tokenizer.apply_chat_template(prompt_with_response, tokenize=False)
                    
                    outputs = model.prompt_logprobs(
                        prompts=[formatted_prompt_with_response],
                        n_logprobs_per_token=args.n_logprobs_per_token,
                    )

                    # single user need to compute logprobs without conv
                    if len(user_list) == 1:
                        prompt_no_conv_without_response = [
                            {"role": "user", "content": conversation["prompt"]},
                            {"role": "assistant", "content": ""},
                        ]
                        prompt_no_conv_with_response = [
                            {"role": "user", "content": conversation["prompt"]},
                            {"role": "assistant", "content": gold_response},
                        ]

                        # format
                        formatted_prompt_no_conv_without_response = tokenizer.apply_chat_template(prompt_no_conv_without_response, tokenize=True)[:-1] # :-1 to ignore eos token
                        formatted_prompt_no_conv_with_response = tokenizer.apply_chat_template(prompt_no_conv_with_response, tokenize=False)

                        outputs_no_conv = model.prompt_logprobs(
                            prompts=[formatted_prompt_no_conv_with_response],
                            n_logprobs_per_token=args.n_logprobs_per_token,
                        )
                        p_gold_no_conv = outputs_no_conv[0].prompt_logprobs[1 + len(formatted_prompt_no_conv_without_response):]
                        p_gold_no_conv = [v.logprob for prob in p_gold_no_conv for _, v in prob.items()]

                    # get p_gold_given_conversation
                    p_gold_given_conversation = outputs[0].prompt_logprobs[1 + len(formatted_prompt_without_response):] 
                    p_gold_given_conversation = [v.logprob for prob in p_gold_given_conversation for _, v in prob.items()]
                    
                    if len(user_list) > 1:
                        logprobs[attempt_key].append(np.mean(p_gold_given_conversation))
                    else:                        
                        # single user need to logprob diff with and without conv                        
                        logprobs[attempt_key].append(np.mean(p_gold_given_conversation) - np.mean(p_gold_no_conv))

    # now compute expected info gain
    eig = {}
    
    for prompt_attempt_user_key, prompt_attempt_user_value in logprobs.items():
        if len(prompt_attempt_user_value) > 1: 
            p_gold_given_prompt = torch.tensor(1/args.n_users_per_prompt).repeat(args.n_users_per_prompt) # baseline: uniform 
            p_gold_given_prompt_entropy = -(p_gold_given_prompt * torch.log(p_gold_given_prompt)).sum()
            p_gold_given_conversation = torch.softmax(torch.tensor(prompt_attempt_user_value), dim=0)
            p_gold_given_conversation_entropy = -(p_gold_given_conversation * torch.log(p_gold_given_conversation)).sum()
            eig[prompt_attempt_user_key] = (p_gold_given_prompt_entropy - p_gold_given_conversation_entropy).item()
            logging.info(eig[prompt_attempt_user_key])
        else:
            logging.info("ONE USER")            
            eig[prompt_attempt_user_key] = prompt_attempt_user_value[0].item()
    
    # score questions based on eig (best question score per prompt across uesrs and attempts)
    best_questions = {}    
    for prompt_id in set(conversations["id"]):
        best_question_eigs = [] # best question attempt 
        questions = []
        responses = []
        users = []
        
        for attempt in set(conversations["attempt"]):   
            
            prompt_attempt_users = [
                int(key.split("_")[3])
                for key in conversation_dict.keys()
                if int(key.split("_")[1]) == prompt_id and 
                int(key.split("_")[-1]) == attempt
            ]
            
            best_question_eig_across_users = [] 
            best_question_responses = []
            
            for j, user_id in enumerate(prompt_attempt_users):
            
                attempt_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
                best_question_eig_across_users.append(eig[attempt_key])
                best_question_responses.append(conversation_dict[attempt_key]["response"])
                
                if j == 0: # first turn question is always the same so only need to append once
                    questions.append(conversation_dict[attempt_key]["question"])
                
                if attempt == 0: 
                    users.append(user_id)
            
            # how much did this attempt help on average across users 
            best_question_eigs.append(np.mean(best_question_eig_across_users))
            responses.append(best_question_responses)
            # print(best_question_eigs)            

        # best attempt across users
        best_question_idx = int(np.argmax(best_question_eigs))        
        # add this to our best questions for each prompt_id 
        best_questions[f"best_question_for_prompt_{prompt_id}"] = {}
        best_questions[f"best_question_for_prompt_{prompt_id}"]['question_performances'] = best_question_eigs
        best_questions[f"best_question_for_prompt_{prompt_id}"]['questions'] = questions
        best_questions[f"best_question_for_prompt_{prompt_id}"]['responses'] = responses[best_question_idx]
        best_questions[f"best_question_for_prompt_{prompt_id}"]['best_question_idx'] = best_question_idx
        best_questions[f"best_question_for_prompt_{prompt_id}"]['best_question'] = questions[best_question_idx]  
        best_questions[f"best_question_for_prompt_{prompt_id}"]['user'] = users

        questions = []
        best_question_eigs = []

    
    with open(args.save_file, "w") as f:
        json.dump(best_questions, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())