"""Expected Info Gain Turn 2."""
import json
import fire
import hydra
import copy
import tqdm
import logging
import numpy as np
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from helpers import *
from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="expected_info_gain_turn_2")
def main(args: DictConfig) -> None:
    logging.info(f"""Computing EIG. Start Prompt: {args.prompt_start}. End Prompt: {args.prompt_end}
Saving to: {args.save_file}
Convo file: {args.conversations}
N_USER: {args.n_users_per_prompt}""")
   
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
    for prompt_id, user_id, prompt, attempt, question_turn_1, response_turn_1, question_turn_2, response_turn_2 in zip(*conversations.values()):
        conversation_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
        conversation_dict[conversation_key] = {
            "prompt": prompt, 
            "question_turn_1": question_turn_1, 
            "response_turn_1": response_turn_1,
            "question_turn_2": question_turn_2, 
            "response_turn_2": response_turn_2,
            }
  

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
            
            for user_id in prompt_attempt_users:
                        
                attempt_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
                
                logprobs[attempt_key] = {}
                   
                gold_response_key = f"{prompt_id}_{user_id}"
                gold_response = gold_responses[gold_response_key]
                
                for other_user_id in prompt_attempt_users:
                    
                    conversation_key = f"prompt_{prompt_id}_user_{other_user_id}_attempt_{attempt}"
                    conversation = conversation_dict[conversation_key]
                    
                    prompt_without_response = [
                        {"role": "user", "content": conversation["prompt"]},
                        {"role": "assistant", "content": conversation["question_turn_1"]},
                        {"role": "user", "content": conversation["response_turn_1"]},
                        {"role": "assistant", "content": conversation["question_turn_2"]},
                        {"role": "user", "content": conversation["response_turn_2"]},
                        {"role": "assistant", "content": ""},
                    ]
                    
                    prompt_with_response = [
                        {"role": "user", "content": conversation["prompt"]},
                        {"role": "assistant", "content": conversation["question_turn_1"]},
                        {"role": "user", "content": conversation["response_turn_1"]},
                        {"role": "assistant", "content": conversation["question_turn_2"]},
                        {"role": "user", "content": conversation["response_turn_2"]},
                        {"role": "assistant", "content": gold_response},
                    ]              
                    
                    
        
                    # format 
                    formatted_prompt_without_response = tokenizer.apply_chat_template(prompt_without_response, tokenize=True)[:-1] # :-1 to ignore eos token
                    formatted_prompt_with_response = tokenizer.apply_chat_template(prompt_with_response, tokenize=False)
                    
                    outputs = model.prompt_logprobs(
                        prompts=[formatted_prompt_with_response],
                        n_logprobs_per_token=args.n_logprobs_per_token,
                    )
                    
                    

                    # get p_gold_given_conversation
                    p_gold_given_conversation = outputs[0].prompt_logprobs[1 + len(formatted_prompt_without_response):] 
                    p_gold_given_conversation = [v.logprob for prob in p_gold_given_conversation for _, v in prob.items()]
                    logprobs[attempt_key][other_user_id] = np.mean(p_gold_given_conversation)
         
    # now compute expected info gain

    eig = {}
    best_attempts = {}
    p_gold_given_prompt = torch.tensor(1/args.n_users_per_prompt).repeat(args.n_users_per_prompt) # baseline: uniform 
    p_gold_given_prompt_entropy = -(p_gold_given_prompt * torch.log(p_gold_given_prompt)).sum()
    
    for prompt_id in tqdm.tqdm(set(conversations["id"])):
        
        prompt_users = [
            int(key.split("_")[3])
            for key in conversation_dict.keys()
            if int(key.split("_")[1]) == prompt_id
        ]
        
        for user_id in prompt_users:
            
            attempt_performances = {}
            
            for attempt in set(conversations["attempt"]):
                
                attempt_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
                
                eig[attempt_key] = {}
                
                p_gold_given_conversation_target_user = logprobs[attempt_key][user_id]
                
                p_gold_given_conversation_other_users = {}
                
                for other_attempt in set(conversations["attempt"]):
                    
                    attempt_key_other_user = f"prompt_{prompt_id}_user_{user_id}_attempt_{other_attempt}"
                    
                    p_gold_given_conversation_other_user = copy.deepcopy(logprobs[attempt_key_other_user])
                    del p_gold_given_conversation_other_user[user_id]
                    
                    p_gold_given_conversation_other_users[other_attempt] = list(p_gold_given_conversation_other_user.values())
                
                for other_attempt_key, other_attempt_val in p_gold_given_conversation_other_users.items():
                    
                    probs = [p_gold_given_conversation_target_user] + other_attempt_val
                    probs = torch.softmax(torch.tensor(probs ), dim=0)
                    conditional_entropy =  -(probs * torch.log(probs)).sum()
                    eig[attempt_key][other_attempt_key] = (p_gold_given_prompt_entropy - conditional_entropy).item()
                    
                attempt_performances[attempt] = np.mean(list(eig[attempt_key].values()))
            
            best_attempts[f"prompt_{prompt_id}_user_{user_id}"] = {}
            best_attempts[f"prompt_{prompt_id}_user_{user_id}"]["eig"] = np.max(list(attempt_performances.values()))
            best_attempts[f"prompt_{prompt_id}_user_{user_id}"]["attempt"] = np.argmax(list(attempt_performances.values()))


    best_questions = {
        'prompt': [],
        'user_id': [],
        'best_question_attempt_id': [],
        'best_question_attempt_eig': [],
        'average_eig_across_users': [],
    }
    for prompt_id in tqdm.tqdm(set(conversations["id"])):
        
        eigs = []
        
        prompt_users = [
            int(key.split("_")[3])
            for key in conversation_dict.keys()
            if int(key.split("_")[1]) == prompt_id
        ]
        
        for user_id in sorted(set(prompt_users)):
            key = f"prompt_{prompt_id}_user_{user_id}"
            val = best_attempts[key]
            eigs.append(val["eig"])
            best_questions['prompt'].append(prompt_id)
            best_questions['user_id'].append(user_id)
            best_questions['best_question_attempt_id'].append(int(val['attempt']))
            best_questions['best_question_attempt_eig'].append(float(val['eig']))
        
        for user_id in sorted(set(prompt_users)):
            best_questions['average_eig_across_users'].append(np.mean(eigs))
            
    # add t
    breakpoint()
    with open(args.save_file, "w") as f:
        json.dump(best_questions, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())