"""Generate personalized responses with oracle (i.e., give the original user + prompt, no questions needed)"""
import json
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="oracle")
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
    
    # users
    with open(args.users, 'r') as f:
        users = json.load(f)
    
    # prompts
    with open(args.prompts, 'r') as f:
        prompts = json.load(f)
        
    # format prompts
    ids = []
    user_ids = []
    batch_prompts = []
    for user_id, user in enumerate([USER_1, USER_2, USER_3, USER_4, USER_5]):
        for i, prompt in enumerate(prompts['prompt'][:args.n_prompts]):
            ids.append(i)
            user_ids.append(user_id)
            batch_prompts.append([{"role": "user", "content": ORACLE_PROMPT.format(user=user, question=prompt)}])

    formatted_batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    
    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    
    # format and write to json
    formatted_responses = [
        response.split('<|end_header_id|>')[1].strip().split('Response:')[1].strip().split('Additional Comments:')[0].strip() 
        for response in batch_responses
    ]
    
    gold_responses = {
        'id': [],
        'user': [],
        'prompt': [],
        'response': [],
    }
    
    for i, user_id, prompt, response in zip(ids, user_ids, batch_prompts, formatted_responses):
        gold_responses['id'].append(i)
        gold_responses['user'].append(user_id)
        gold_responses['prompt'].append(prompt)
        gold_responses['response'].append(response)
    
    with open('data/gold_responses.json', 'w') as f:
        json.dump(gold_responses, f, indent=4)
  

if __name__ == "__main__":
    fire.Fire(main())