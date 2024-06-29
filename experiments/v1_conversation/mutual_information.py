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


@hydra.main(version_base=None, config_path="config", config_name="mutual_information")
def main(args: DictConfig) -> None:
    
    torch.manual_seed(args.seed)
   
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
    with open(args.prompts, 'r') as f:
        prompts = json.load(f)
        
    # users
    with open(args.users, 'r') as f:
        users = json.load(f)
        
    # only keep up to max users
    users = {
        k: v for k, v in users.items() 
        if int(k.split("_")[1]) < args.n_users
    }
        
    # logprobs container
    all_logprobs = {}
    
    for i, (prompt, response) in tqdm.tqdm(enumerate(
        zip(prompts['prompt'][:args.n_prompts], prompts['response'][:args.n_prompts])
    )):
        
        all_logprobs[i] = {
            'prompt': prompt, 
            'response': response, 
            'means': [],
            'mutual_information': 0,
        }
        
        # rand_user_ids = torch.randperm(args.n_users)[:args.n_users_per_prompt].tolist()
        # 
        rand_user_ids = [4, ] # users that are different from each other 
        
        for j, rand_user_id in enumerate(rand_user_ids):
            
            user = users[f"user_{rand_user_id}"]
            
            # prompt with no assistant response 
            prompt_without_response = [
                    {"role": "user", "content": PROMPT_LOGPROBS.format(user=user, question=prompt)},
            ]
            
            # prompt with assistant response 
            prompt_with_response = [
                    {"role": "user", "content": PROMPT_LOGPROBS.format(user=user, question=prompt)},
                    {"role": "assistant", "content": response}
            ]
            
            # format 
            formatted_prompt_without_response = tokenizer.apply_chat_template(prompt_without_response, tokenize=True)
            formatted_prompt_with_response = tokenizer.apply_chat_template(prompt_with_response, tokenize=False)

            outputs = model.prompt_logprobs(
                prompts=[formatted_prompt_with_response],
                n_logprobs_per_token=args.n_logprobs_per_token,
            )

            # get only logprobs for response
            logprobs = outputs[0].prompt_logprobs[1 + len(formatted_prompt_without_response):] # type is dict so need to extract vals
            logprobs = [v for prob in logprobs for k, v in prob.items()]
            all_logprobs[i]['means'].append(np.mean(logprobs))
        
        all_logprobs[i]['mutual_information']  = mutual_information(
            logprobs=torch.tensor(all_logprobs[i]['means']),
            n_users=args.n_users_per_prompt,
        ).numpy().item()
       
    with open(args.save_file, 'w') as f:
        json.dump(all_logprobs, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())