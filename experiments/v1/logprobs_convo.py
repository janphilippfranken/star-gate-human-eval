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

N_USERS = 5

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
    with open(args.gold_responses, 'r') as f:
        gold_responses = json.load(f)
        
    gold_responses = {
        f"{prompt_id}_{user_id}": gold_response for prompt_id, user_id, _, gold_response in
        zip(*gold_responses.values())
    }
        
    # conversations
    with open(args.conversations, 'r') as f:
        conversations = json.load(f)
        
    # logprobs container
    all_logprobs = {}
    logps_only = {}
    
    for i, (prompt_id, user_id, prompt, attempt, question, response) in tqdm.tqdm(enumerate(zip(*conversations.values()))):
        
        gold_key =  f"{prompt_id}_{user_id}"
        gold_response = gold_responses[gold_key]
        
        attempt_key = f"prompt_{prompt_id}_attempt_{attempt}"
        if attempt_key not in logps_only:
            logps_only[attempt_key] = {'base': [], 'question': []}
        
        all_logprobs[i] = {
            'id': prompt_id,
            'user': user_id,
            'prompt': prompt, 
            'attempt': attempt, 
            'question': question,
            'response': response, 
            'logprobs': None,
        }
        
        # baselines without question:
        base_prompt_without_response = [
            {"role": "user", "content": prompt},
        ]
        
        # prompt with assistant response 
        base_prompt_with_response = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": gold_response},
        ]
        
        # prompt with no assistant response 
        prompt_without_response = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": question},
            {"role": "user", "content": response},
        ]
        
        # prompt with assistant response 
        prompt_with_response = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": question},
            {"role": "user", "content": response},
            {"role": "assistant", "content": gold_response},
        ]
        
        # format 
        formatted_base_prompt_without_response = tokenizer.apply_chat_template(base_prompt_without_response, tokenize=True)
        formatted_base_prompt_with_response = tokenizer.apply_chat_template(base_prompt_with_response, tokenize=False)
        
        formatted_prompt_without_response = tokenizer.apply_chat_template(prompt_without_response, tokenize=True)
        formatted_prompt_with_response = tokenizer.apply_chat_template(prompt_with_response, tokenize=False)

        base_outputs = model.prompt_logprobs(
            prompts=[formatted_base_prompt_with_response],
            n_logprobs_per_token=args.n_logprobs_per_token,
        )
        
        outputs = model.prompt_logprobs(
            prompts=[formatted_prompt_with_response],
            n_logprobs_per_token=args.n_logprobs_per_token,
        )

        # get only logprobs for response
        logprobs_base = base_outputs[0].prompt_logprobs[1 + len(formatted_base_prompt_without_response):] # type is dict so need to extract vals
        logprobs_base = [v for prob in logprobs_base for k, v in prob.items()]
        logps_only[attempt_key]['base'].append(np.mean(logprobs_base))
        
        # w questions
        logprobs = outputs[0].prompt_logprobs[1 + len(formatted_prompt_without_response):] # type is dict so need to extract vals
        logprobs = [v for prob in logprobs for k, v in prob.items()]
        all_logprobs[i]['logprobs'] = np.mean(logprobs)
        logps_only[attempt_key]['question'].append(np.mean(logprobs))
        
    eig = {}
    
    for prompt_attempt, attempt_probs in logps_only.items():
        base_probs = torch.softmax(torch.tensor(attempt_probs['base']), dim=0)
        base_entropy = -(base_probs * torch.log(base_probs)).sum()
        question_probs = torch.softmax(torch.tensor(attempt_probs['question']), dim=0)
        question_entropy = -(question_probs * torch.log(question_probs)).sum()
        eig[prompt_attempt] = base_entropy - question_entropy
    
    breakpoint()

    
    
    
    #     all_logprobs[i]['mutual_information']  = mutual_information(
    #         logprobs=torch.tensor(all_logprobs[i]['means']),
    #         n_users=N_USERS,
    #     ).numpy().item()
       
        
    # breakpoint() 
            
    # with open('logprobs_mi.json', 'w') as f:
    #     json.dump(all_logprobs, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())