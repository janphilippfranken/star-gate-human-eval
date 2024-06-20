""""""
import json
import fire
import hydra
import tqdm
import logging
import numpy as np
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from helpers import *
from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="expected_info_gain")
def main(args: DictConfig) -> None:
    logging.info(f"""Computing EIG. Start Prompt: {args.prompt_start}. End Prompt: {args.prompt_end}
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
    for prompt_id, user_id, user, prompt, attempt, question, response in zip(*conversations.values()):
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
            
            for user_id in prompt_attempt_users:
                        
                attempt_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
                
                logprobs[attempt_key] = []
                   
                # now to get the distributions of the above logprobs for each attempt_key, we need to compute logprobs across gold responses for each user 
                for other_user_id in prompt_attempt_users:
                    
                    conversation_key = f"prompt_{prompt_id}_user_{other_user_id}_attempt_{attempt}"
                    gold_response_key = f"{prompt_id}_{user_id}"
                    
        
                    conversation = conversation_dict[conversation_key]
                        
                    gold_response = gold_responses[gold_response_key] 
        
                    # prompt with no assistant response 
                    prompt_without_response = [
                        {"role": "user", "content": conversation["prompt"]},
                        {"role": "assistant", "content": conversation["question"]},
                        {"role": "user", "content": conversation["response"]},
                    ]
                    
                    # prompt with assistant response 
                    prompt_with_response = [
                        {"role": "user", "content": conversation["prompt"]},
                        {"role": "assistant", "content": conversation["question"]},
                        {"role": "user", "content": conversation["response"]},
                        {"role": "assistant", "content": gold_response},
                    ]
        
                    # format 
                    formatted_prompt_without_response = tokenizer.apply_chat_template(prompt_without_response, tokenize=True)
                    formatted_prompt_with_response = tokenizer.apply_chat_template(prompt_with_response, tokenize=False)
                    
                    outputs = model.prompt_logprobs(
                        prompts=[formatted_prompt_with_response],
                        n_logprobs_per_token=args.n_logprobs_per_token,
                    )

                    # get p_gold_given_conversation
                    p_gold_given_conversation = outputs[0].prompt_logprobs[1 + len(formatted_prompt_without_response):] # type is dict so need to extract vals
                    p_gold_given_conversation = [v for prob in p_gold_given_conversation for _, v in prob.items()]
                    logprobs[attempt_key].append(np.mean(p_gold_given_conversation))
    

if __name__ == "__main__":
    fire.Fire(main())