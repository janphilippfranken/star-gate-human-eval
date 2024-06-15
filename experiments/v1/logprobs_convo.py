"""Get logprobs of assistant responses."""
import json
import fire
import hydra
import tqdm
import numpy as np
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from helpers import *
from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="logprobs_convo")
def main(args: DictConfig) -> None:
   
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
        
        for user_id in set(conversations["user"]): 
        
            for attempt in set(conversations["attempt"]):
                        
                attempt_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
                
                logprobs[attempt_key] = []
                   
                # now to get the distributions of the above logprobs for each attempt_key, we need to compute logprobs across gold responses for each user 
                for other_user_id in set(conversations["user"]):
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
    # breakpoint()
    eig = {}
    # breakpoint()
    
    for prompt_user_attempt_key, prompt_user_attempt_value in logprobs.items():
        p_gold_given_prompt = torch.tensor(1/args.n_users).repeat(args.n_users) # just uniform in the beginning
        p_gold_given_prompt_entropy = -(p_gold_given_prompt * torch.log(p_gold_given_prompt)).sum()
        p_gold_given_conversation = torch.softmax(torch.tensor(prompt_user_attempt_value), dim=0)
        p_gold_given_conversation_entropy = -(p_gold_given_conversation * torch.log(p_gold_given_conversation)).sum()
        eig[prompt_user_attempt_key] = (p_gold_given_prompt_entropy - p_gold_given_conversation_entropy).item()
    
    best_questions = {}
    for prompt_id in set(conversations["id"]): 
        attempt_prompt_scores = []
        for user_id in set(conversations["user"]): 
            attempt_user_scores = []
            for attempt in set(conversations["attempt"]):
                attempt_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
                attempt_user_scores.append(eig[attempt_key])
            attempt_prompt_scores.append(np.argmax(attempt_user_scores))
        best_questions[f"best_question_for_prompt_{prompt_id}"] = int(np.argmax(np.bincount(attempt_prompt_scores)))
    
        
    breakpoint() 
            
    with open("data/best_questions_idx.json", "w") as f:
        json.dump(best_questions, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())