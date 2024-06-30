"""Generate responses and logprobs."""
import json
import fire
import tqdm
import hydra
import numpy as np 
from omegaconf import DictConfig
from datasets import load_dataset
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from helpers import *
from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="base_responses_base_model")
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
        batch_prompts.append(RESPONSE_PROMPT_BASE.format(question=dataset['question'][i]))
        
        
    # responses
    batch_responses = model.batch_prompt(
        prompts=batch_prompts,
        **args.generation_config,
    )
    
    formatted_responses = [format_response(response) for response in batch_responses]
    extracted_responses = [extract_answer(response) for response in formatted_responses]
    gt_answers = [int(gt_answer.split('####')[1].strip().lower().replace(",", "")) for gt_answer in dataset['answer']]
    evaluated_responses = [evaluate_model_response(model_answer, gt) for model_answer, gt in zip(extracted_responses, gt_answers)]
    print(np.mean(evaluated_responses))
    
    
    breakpoint()
    
    
    # format
        
    with open(args.save_file, "w") as f:
        json.dump(evaluated_responses, f, indent=4)    


if __name__ == "__main__":
    fire.Fire(main())