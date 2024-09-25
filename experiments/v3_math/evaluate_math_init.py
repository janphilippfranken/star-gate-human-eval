import json
import re 
import fire
import random
import hydra
import torch
from omegaconf import DictConfig
from transformers import AutoTokenizer

import logging

from datasets import load_dataset

from stargate.vllm_inference_model import VLLMInferenceModel
from dataset.util import clean_numbers, last_boxed_only, last_boxed_only_string, remove_boxed
from dataset.math_equivalence import is_equiv


PROMPT = """Solve the following math problem step by step. The last line of your response should be of the form Answer: $ANSWER (without quotes) where $ANSWER is the answer to the problem.

{question}

Remember to put your answer on its own line after "Answer:", and you do not need to use a \\boxed command."""


@hydra.main(version_base=None, config_path="config", config_name="evaluate")
def main(args: DictConfig) -> None:
    
    torch.manual_seed(42)
    random.seed(42)
    
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
    dataset = load_dataset(
        "hendrycks/competition_math",
        split="test",
        cache_dir="./data/math",
    )
    
    problems = [datum["problem"] for datum in dataset]
    solutions = [datum["solution"] for datum in dataset]
    answer_strings = [remove_boxed(last_boxed_only_string(solution)) for solution in solutions]
    breakpoint()
    
    prompts = [PROMPT.format(question=question) for question in problems[:args.end_prompts]]
    
    prompts = [
        [{"role": "user", "content": prompt}]
        for prompt in prompts
    ]

    formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in prompts
    ]
    
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    
    batch_responses = [
        response.split("<|start_header_id|>assistant<|end_header_id|>")[1].strip()
        for response in batch_responses   
    ]
   
    formatted_batch_responses = []
    
    for response in batch_responses:
        try:
            formatted_batch_responses.append(response.split("\n\nAnswer:")[1].strip())
        except:
            formatted_batch_responses.append("Null")

    response_scores = []
    response_rationales = []
    
    for i in range(args.end_prompts):
        response = formatted_batch_responses[i]
        try:
            res = is_equiv(response, answer_strings[i]) 
            
            response_scores.append(int(res))
        except:
            response_scores.append(0)

    print(sum(response_scores)/len(response_scores))
if __name__ == "__main__":
    fire.Fire(main())