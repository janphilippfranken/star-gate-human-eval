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

def evalaute_and_format(model, tokenizer, batch_prompts, config, type='base'):
    
    if type == "base":
        formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts
        ]
        
        batch_responses = model.batch_prompt(
            prompts=formatted_batch_prompts, 
            **config
        )
        
        formatted_responses = [
            response.split('<|end_header_id|>')[1].strip() 
            for response in batch_responses
        ]
        

    if type == "cot":
        formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts
        ]
        
        batch_responses = model.batch_prompt(
            prompts=formatted_batch_prompts, 
            **config
        )
        
        formatted_responses = [
            response.split('<|end_header_id|>')[1].strip() 
            for response in batch_responses
        ]
        
        final_answers = []
        for response in formatted_responses:
            try:
                final_answers.append(response.split("Final Answer:")[1].strip())
            except:
                print("INVALID")
                final_answers.append(response)
                
        formatted_responses = final_answers
        
    elif type == "test":
        formatted_batch_prompts = [
            tokenizer.apply_chat_template(prompt, tokenize=False) 
            for prompt in batch_prompts
        ]
       
        formatted_batch_prompts = [
            '<|eot_id|>'.join(prompt.split('<|eot_id|>')[:-1])
                for prompt in formatted_batch_prompts 
        ]
    
        batch_responses = model.batch_prompt(
            prompts=formatted_batch_prompts, 
            **config
        )
        
        formatted_responses = [
            response.strip() for response in batch_responses
        ]
        
    
    extracted_responses = [
        extract_answer(response) 
        for response in formatted_responses
    ]
    
    return extracted_responses, formatted_responses
    
    

@hydra.main(version_base=None, config_path="config", config_name="evaluate")
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
    
    # rationales 
    rationales = json.load(open(args.rationales, "r"))
    
    
    # prompts 
    batch_prompts_0shot = []
    for i in range(args.n_prompts):
        batch_prompts_0shot.append([
            {"role": "user", "content": RESPONSE_PROMPT.format(question=dataset['question'][i])}
        ])
        
    batch_prompts_cot = []
    for i in range(args.n_prompts):
        batch_prompts_cot.append([
            {"role": "user", "content": RATIONALE_PROMPT.format(question=dataset['question'][i])}
        ])
        
    batch_prompts_best = []
    for i in range(args.n_prompts):
        batch_prompts_best.append([
            {"role": "user", "content": EVALUATION_PROMPT_HUMAN.format(question=dataset['question'][i])},
            {"role": "assistant", "content": EVALUATION_PROMPT_ASSISTANT.format(rationale=rationales[str(i)]["best_rationale_ce"])}
        ])
        
    batch_prompts_worst = []
    for i in range(args.n_prompts):
        batch_prompts_worst.append([
            {"role": "user", "content": EVALUATION_PROMPT_HUMAN.format(question=dataset['question'][i])},
            {"role": "assistant", "content": EVALUATION_PROMPT_ASSISTANT.format(rationale=rationales[str(i)]["worst_rationale_ce"])}
        ])

    
   
    # get gt answers from dataset 
    gt_answers = [
        round(float(gt_answer.split('####')[1].strip().lower().replace(",", "")), 1)
        for gt_answer in dataset['answer'][:args.n_prompts]
    ]
    

    # responses_0shot, f0shot = evalaute_and_format(model, tokenizer, batch_prompts_0shot, args.generation_config)
    # responses_cot, fcot = evalaute_and_format(model, tokenizer, batch_prompts_cot, args.generation_config, type='cot')
    responses_best, fbest = evalaute_and_format(model, tokenizer, batch_prompts_best, args.generation_config, type='test')
    responses_worst, fworst = evalaute_and_format(model, tokenizer, batch_prompts_worst, args.generation_config, type='test')
    breakpoint()
    
    
    # results_0shot = [evaluate_model_response(model_answer, gt) for model_answer, gt in zip(responses_0shot, gt_answers)]
    # results_cot = [evaluate_model_response(model_answer, gt) for model_answer, gt in zip(responses_cot, gt_answers)]
    # print(np.mean(results_0shot), np.mean(results_cot))
    # breakpoint()
    results_best = [evaluate_model_response(model_answer, gt) for model_answer, gt in zip(responses_best, gt_answers)]
    results_worst = [evaluate_model_response(model_answer, gt) for model_answer, gt in zip(responses_worst, gt_answers)]
    
    print(np.mean(results_best), np.mean(results_worst))
    breakpoint()
    # with open(args.save_file, "w") as f:
    #     json.dump(evaluated_responses, f, indent=4)    


if __name__ == "__main__":
    fire.Fire(main())