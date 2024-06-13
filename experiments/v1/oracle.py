import json
import fire
import random
import hydra
import re
import numpy as np
import os
from omegaconf import DictConfig
from tqdm import tqdm
import torch
from datasets import load_dataset
from stargate.vllm_inference_model import VLLMInferenceModel
from transformers import AutoTokenizer



N_ITEMS = 2000
CoT = False

PROMPT_INSTRUCT = """Respond to the query below. Format your answer as follows:

Q: <query here>
A: <your final answer here>

Q: {question}"""


def format_response(response):
    formatted_response = ""
    try:
        formatted_response = response.split("A:")[1].strip().lower()
    except:
        print("invalid, continue")
    return formatted_response

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


# main evaluation script
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
    # breakpoint()
    batch_prompts = ["How do I make the perfect chocolate chip cookie?"]
    batch_prompts = [[{"role" : "user", "content": prompt}] for prompt in batch_prompts]
    batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    # breakpoint()
    batch_responses = model.batch_prompt(
        prompts=batch_prompts,
        **args.generation_config,
    )
  

if __name__ == "__main__":
    fire.Fire(main())