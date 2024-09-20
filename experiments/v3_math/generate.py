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

PROMPT = """Q: {question}\nA:"""

TRAIN_PROMPT = """<plan>
I will first generate exactly 4 answer options. I will then pick the best answer.
</plan>

<answer_options>
{responses}
</answer_options>

<best_answer>
{correct_response}
</best_answer>"""

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


@hydra.main(version_base=None, config_path="config", config_name="generate")
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
        split="train",
        cache_dir="./data/gsm",
    )
    
    gt_answers = [
        int(gt_answer.split('####')[1].strip().lower().replace(",", "")) for gt_answer in dataset['answer']
    ]
    
    prompts = [PROMPT.format(question=question) for question in dataset['question'][:args.end_prompts]]
    
    extended_prompts = []
    
    for prompt in prompts:
        for _ in range(args.n_return):
            extended_prompts.append(prompt)
    
    prompts = [
        [{"role": "user", "content": prompt}]
        for prompt in extended_prompts
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
    
    for i in range(args.end_prompts):
        responses = [] 
        for j in range(args.n_return):
            responses.append(batch_responses[j + i * args.n_return])
        formatted_batch_responses.append(responses)
        
    response_scores = [[] for _ in range(args.end_prompts)]
    
    for i in range(args.end_prompts):
        responses = formatted_batch_responses[i]
        for response in responses:
            try:
                answer = extract_answer(answer=response)
                res = evaluate_model_response(answer, gt_answers[i]) 
                response_scores[i].append(int(res))
            except:
                response_scores[i].append(0)

    with open(args.save_file_scores, "w") as f:
        json.dump(response_scores, f, indent=4)
    
    with open(args.save_file_responses, "w") as f:
        json.dump(formatted_batch_responses, f, indent=4)
        
    train_data = []
    
    
    for i in range(args.end_prompts):
        if sum(response_scores[i]) == 0:
            continue
        else:
            correct_indices = [k for k, score in enumerate(response_scores[i]) if score == 1]
            correct_response = random.choice(correct_indices)
            responses = "\n\n".join(
                [f"Answer {j + 1}: {formatted_batch_responses[i][j]}" for j in range(args.n_return)]
            ).strip()

            train_data.append([
                {"role": "user", "content": f"Q: {dataset['question'][i]}\nA:"},
                {"role": "assistant", "content": TRAIN_PROMPT.format(responses=responses, correct_response=f"Answer {correct_response + 1}: {formatted_batch_responses[i][correct_response]}")},
            ])

    
    with open(args.save_train_responses, "w") as f:
        json.dump(train_data, f, indent=4)
                

if __name__ == "__main__":
    fire.Fire(main())