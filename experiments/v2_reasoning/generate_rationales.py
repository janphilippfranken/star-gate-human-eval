"""Generate responses and logprobs."""
import json
import fire
import hydra
import numpy as np 
from omegaconf import DictConfig
from datasets import load_dataset
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from helpers import *
from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="generate_rationales")
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
    
    # data 
    dataset = load_dataset(
        "gsm8k",
        "main",
        split=args.dataset_split,
        cache_dir=args.cache_dir,
    )
    
    # prompts 
    batch_prompts = []
    for i in range(args.n_prompts):
        batch_prompts.append([
            {"role": "user", "content": RATIONALE_PROMPT.format(question=dataset['question'][i])}
        ])

    formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts
    ]
    
    # responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    
    # format
    formatted_responses = [
        response.split('<|end_header_id|>')[1].strip().split("Rationale:")[1].strip()
        for response in batch_responses
    ]
    
    breakpoint()

    # eval respons 


if __name__ == "__main__":
    fire.Fire(main())