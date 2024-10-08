"""Generate Gold Responses: g_ij ~ model(g | x_i, u_j)"""
import json
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

import logging

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="gold_responses")
def main(args: DictConfig) -> None:
    
    logging.info(args)

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
        

    prompt_ids = []
    user_ids = []
    batch_prompts = []
    opening_prompts = []
    
    for user_id, user in enumerate(list(users.values())[:args.n_users]):
        # @TODO: Temp, needs fix        
        # if user_id in [4, 17]:
        # if user_id in args.chosen_users:
        for i, prompt in enumerate(prompts[args.start_prompts:args.end_prompts]):
            prompt_ids.append(i + args.start_prompts)
            user_ids.append(user_id)
            opening_prompts.append(prompt)

            batch_prompts.append([
                {"role": "user", "content": ORACLE_PROMPT.format(prompt=prompt, user=user)}
            ])

        
    formatted_batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    logging.info(len(formatted_batch_prompts))

    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    # format and write to json
    formatted_responses = []
    for response in batch_responses:
        try:
            formatted_responses.append(response.split("<|end_header_id|>")[1].strip().split("Response:")[1].strip().split("Additional Comments:")[0].strip())
        except:
            formatted_responses.append("<|invalid_response|>")
            print(f"INVALID RESPONSE: {response.split('<|end_header_id|>')[1].strip()}")

    gold_responses = {
        "prompt_id": [],
        "user_id": [],
        "prompt": [],
        "response": [],
    }
    
    for i, user_id, prompt, response in zip(prompt_ids, user_ids, opening_prompts, formatted_responses):
        gold_responses["prompt_id"].append(i)
        gold_responses["user_id"].append(user_id)
        gold_responses["prompt"].append(prompt)
        gold_responses["response"].append(response)
    
    with open(args.save_file, "w") as f:
        json.dump(gold_responses, f, indent=4)
  

if __name__ == "__main__":
    fire.Fire(main())