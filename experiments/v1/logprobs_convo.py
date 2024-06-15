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

@hydra.main(version_base=None, config_path="config", config_name="logprobs")
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
    
    # prompts
    with open(args.prompts, 'r') as f:
        prompts = json.load(f)
        
    # logprobs container
    all_logprobs = {}
    
    for i, (prompt, response) in tqdm.tqdm(enumerate(
        zip(prompts['prompt'][:args.n_prompts], prompts['response'][:args.n_prompts])
    )):
        
        all_logprobs[i] = {
            'prompt': prompt, 
            'response': response, 
            'prompt_with_each_user': {},
            'logprobs_for_each_user': {},
            'means': [],
            'variance': 0,
            'mutual_information': 0,
        }
        
        for j, user in enumerate([USER_1, USER_2, USER_3, USER_4, USER_5]):
            # prompt with no assistant response 
            prompt_without_response = [
                    {"role": "user", "content": PROMPT_LOGPROBS.format(user=user, question=prompt[0]['content'])},
            ]
            
            # prompt with assistant response 
            prompt_with_response = [
                    {"role": "user", "content": PROMPT_LOGPROBS.format(user=user, question=prompt[0]['content'])},
                    {"role": "assistant", "content": response}
            ]
            
            # append prompt
            all_logprobs[i]['prompt_with_each_user'][j] = prompt_with_response
            
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
            all_logprobs[i]['logprobs_for_each_user'][j] = logprobs
            all_logprobs[i]['means'].append(np.mean(logprobs))
        
        
        all_logprobs[i]['variance'] = np.var(all_logprobs[i]['means'])
        
        all_logprobs[i]['mutual_information']  = mutual_information(
            logprobs=torch.tensor(all_logprobs[i]['means']),
            n_users=N_USERS,
        ).numpy().item()
       
        
    breakpoint() 
            
    with open('logprobs_mi.json', 'w') as f:
        json.dump(all_logprobs, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())