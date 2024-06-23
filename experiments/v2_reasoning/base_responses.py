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


@hydra.main(version_base=None, config_path="config", config_name="base_responses")
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
            {"role": "user", "content": RESPONSE_PROMPT.format(question=dataset['question'][i])}
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
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses
    ]
    
    # extract final answer 
    extracted_responses = [
        extract_answer(response) 
        for response in formatted_responses
    ]
    
    # get gt answers from dataset 
    gt_answers = [
        [round(float(gt_answer.split('####')[1].strip().lower().replace(",", "")), 1)] * args.n_shots 
        for gt_answer in dataset['answer'][:args.n_prompts]
    ]

    # eval responses 
    evaluated_responses = {}


    # loop over prompts 
    for i in tqdm.tqdm(range(args.n_prompts)):
        
        results = []
        responses = []
        average_logprobs = []

        # loop over shots per prompt 
        for shot in range(args.n_shots):
            # get model answer which is length  args.n_prompts * args.n_shots
            model_answer = extracted_responses[i * args.n_shots + shot]
            gt = gt_answers[i][shot] 
            result = evaluate_model_response(model_answer, gt)
            results.append(result)
            responses.append(formatted_responses[i * args.n_shots + shot])
            
            # get logprobs 
            prompt_without_response = [
                    {"role": "user", "content": RESPONSE_PROMPT.format(question=dataset['question'][i])},
            ]
            
            prompt_with_response = [
                    {"role": "user", "content": RESPONSE_PROMPT.format(question=dataset['question'][i])},
                    {"role": "assistant", "content": formatted_responses[i * args.n_shots + shot]}
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
            average_logprobs.append(np.mean(logprobs))


        evaluated_responses[i] = {  
            "prompt": RESPONSE_PROMPT.format(question=dataset['question'][i]),
            "result": results,
            "response": responses,
            "percentage_correct": sum(results)/args.n_shots,
            "response_logprobs": average_logprobs,
        }
        
    with open(args.save_file, "w") as f:
        json.dump(evaluated_responses, f, indent=4)    


if __name__ == "__main__":
    fire.Fire(main())