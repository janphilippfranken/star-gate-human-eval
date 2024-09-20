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

PROMPT = """Generate eight diverse answer options to the query below. Answers must be distinct and you are not allowed to repeat the same answer multiple times. After you are done generating eight diverse answer options, pick the best one.\n\nQ: {question}\nA:"""

def extract_output(response, key):
    escaped_key = re.escape(key)
    pattern = rf"<{escaped_key}>(.*?)</{escaped_key}>"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return f"{key.capitalize()} tag not found in the response."

def extract_answer(answer):
    if '=' in answer:
        answer = answer.split('=')[-1].strip()
    answer = answer.replace(",", "")
    try:
        answer = re.findall(r"\d+", answer.strip())[-1]
        answer = int(answer)
    except:
        answer = "[invalid]"
    return answer

def evaluate_model_response(model_answer, gt_answer):
    try:
        result = int(model_answer) == int(gt_answer)
        return result
    except:
        return False


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
        "gsm8k",
        "main",
        split="test",
        cache_dir="./data/gsm",
    )
    
    gt_answers = [
        int(gt_answer.split('####')[1].strip().lower().replace(",", "")) for gt_answer in dataset['answer']
    ]
    
    prompts = [PROMPT.format(question=question) for question in dataset['question'][:args.end_prompts]]
    
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
    
    # batch_responses = [
    #     response.split("<|start_header_id|>assistant<|end_header_id|>")[1].strip()
    #     for response in batch_responses   
    # ]
    breakpoint()
    batch_responses = [
        response.strip()
        for response in batch_responses
    ]
    breakpoint()
    formatted_batch_responses = [response for response in batch_responses]

    # extract_output(response, key="best_answer")
    response_scores = []
    
    for i in range(args.end_prompts):
        response = formatted_batch_responses[i]
        try:
            answer = extract_answer(answer=response)
            res = evaluate_model_response(answer, gt_answers[i]) 
            
            response_scores.append(int(res))
        except:
            response_scores.append(0)

    breakpoint()
                

if __name__ == "__main__":
    fire.Fire(main())