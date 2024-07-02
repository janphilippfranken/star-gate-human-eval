"""MI of responses given convos."""
import json
import fire
import hydra
import tqdm
import logging
import torch
import numpy as np
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from helpers import *
from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="mutual_information_from_conversation")
def main(args: DictConfig) -> None:
    logging.info(f"""Computing MI from Convo.
Saving to: {args.save_file}
Convo file: {args.conversations}""")
   
    # model
    model = VLLMInferenceModel(
        **args.model_config
    )
    
    # tokenizer 
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=args.model_config.model,
        cache_dir=args.model_config.download_dir,
    )
    
    # base_ esponses 
    with open(args.base_responses, "r") as f:
        base_responses = json.load(f)["response"]
        
    # conversations
    with open(args.conversations, "r") as f:
        conversations = json.load(f)
        
    conversation_dict = {}
    for prompt_id, user_id, _, prompt, attempt, question, response in zip(*conversations.values()):
        conversation_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
        conversation_dict[conversation_key] = {"prompt": prompt, "question": question, "response": response}
  
    # logprobs container
    logprobs = {}

    for prompt_id in tqdm.tqdm(list(set(conversations["id"]))[:args.n_prompts]):
        
        base_response = base_responses[prompt_id]
        
        for attempt in set(conversations["attempt"]):
            
            prompt_attempt_users = [
                int(key.split("_")[3])
                for key in conversation_dict.keys()
                if int(key.split("_")[1]) == prompt_id and 
                int(key.split("_")[-1]) == attempt
            ]
            
            attempt_key = f"prompt_{prompt_id}_attempt_{attempt}"
            logprobs[attempt_key] = []
            
            for user_id in prompt_attempt_users:
  
                conversation_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
                conversation = conversation_dict[conversation_key]
                
                # prompt with no assistant response 
                # prompt_without_response = [
                #     {"role": "user", "content": conversation["prompt"]},
                #     {"role": "assistant", "content": conversation["question"]},
                #     {"role": "user", "content": conversation["response"]},
                # ]
                prompt_f = PROMPT_LOGPROBS_2.format(
                    prompt=conversation["prompt"], 
                    question=conversation["question"], 
                    response=conversation["response"])
                
                prompt_without_response = [
                    {"role": "user", "content": prompt_f},
                ]
                
                # prompt with assistant response 
                prompt_with_response = [
                    {"role": "user", "content": prompt_f},
                    {"role": "assistant", "content": base_response},
                ]
                
        
                # format 
                formatted_prompt_without_response = tokenizer.apply_chat_template(prompt_without_response, tokenize=True)
                formatted_prompt_with_response = tokenizer.apply_chat_template(prompt_with_response, tokenize=False)
                    
                outputs = model.prompt_logprobs(
                    prompts=[formatted_prompt_with_response],
                    n_logprobs_per_token=args.n_logprobs_per_token,
                )

                # get p_base_given_conversation
                p_base_given_conversation = outputs[0].prompt_logprobs[1 + len(formatted_prompt_without_response):] 
                p_base_given_conversation = [v for prob in p_base_given_conversation for _, v in prob.items()]
                logprobs[attempt_key].append(np.mean(p_base_given_conversation))

    # breakpoint()
    # now compute mis
    mis = {}
    
    for prompt_attempt_key, prompt_attempt_value in logprobs.items():
        mi = mutual_information(logprobs=torch.tensor(prompt_attempt_value), n_users=len(prompt_attempt_value))
        mis[prompt_attempt_key] = mi.item()

    best_questions = {}

    for prompt_id in list(set(conversations["id"]))[:args.n_prompts]:
        question_mis = [] # best question attempt 
        questions = []
        
        for attempt in set(conversations["attempt"]):   
            
            prompt_attempt_users = [
                int(key.split("_")[3])
                for key in conversation_dict.keys()
                if int(key.split("_")[1]) == prompt_id and 
                int(key.split("_")[-1]) == attempt
            ]
            
            conversation_key = f"prompt_{prompt_id}_user_{prompt_attempt_users[0]}_attempt_{attempt}"
            attempt_key = f"prompt_{prompt_id}_attempt_{attempt}"
            question_mis.append(mis[attempt_key])
            questions.append(conversation_dict[conversation_key]["question"])
            
     
        # best attempt across users
        best_question_idx = int(np.argmax(question_mis))
        worst_question_idx =  int(np.argmin(question_mis))
      
        best_question_idx_wo_pos_control = 1 + int(np.argmax(question_mis[1:])) # look at best excluding the first two
    
        # add this to our best questions for each prompt_id 
        best_questions[f"best_question_for_prompt_{prompt_id}"] = {}
        best_questions[f"best_question_for_prompt_{prompt_id}"]['question_performances'] = question_mis
        best_questions[f"best_question_for_prompt_{prompt_id}"]['questions'] = questions
        best_questions[f"best_question_for_prompt_{prompt_id}"]['best_question_idx'] = best_question_idx
        best_questions[f"best_question_for_prompt_{prompt_id}"]['worst_question_idx'] = worst_question_idx
        best_questions[f"best_question_for_prompt_{prompt_id}"]['best_question_idx_wo_pos_control'] = best_question_idx_wo_pos_control 
        best_questions[f"best_question_for_prompt_{prompt_id}"]['best_question'] = questions[best_question_idx]
        best_questions[f"best_question_for_prompt_{prompt_id}"]['best_question_wo_pos_control'] = questions[best_question_idx_wo_pos_control]
        best_questions[f"best_question_for_prompt_{prompt_id}"]['worst_question'] = questions[worst_question_idx]
        

    with open(args.save_file, "w") as f:
        json.dump(best_questions, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())