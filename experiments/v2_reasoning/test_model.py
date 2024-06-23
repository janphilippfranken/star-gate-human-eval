"""Generate generic responses without additional info or questions."""
import json
import fire
import re
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from datasets import load_dataset

from stargate.vllm_inference_model import VLLMInferenceModel

PROMPT = """Q: {question}\nA:"""


def format_response(response):
    formatted_response = ""
    try:
        formatted_response = response.split("Q:")[0].strip().lower()
    except:
        print("invalid, continue")
    return formatted_response

def extract_answer(answer):
    if '=' in answer:
        answer = answer.split('=')[-1].strip()
    answer = answer.replace(",", "")
    try: 
        answer = re.findall(r'\d+\.\d+|\d+', answer.strip())[-1]
        answer = round(float(answer), 1)
    except:
        answer = "[invalid]"
    
    return answer

def evaluate_model_response(model_answer, gt_answer):
    try:
        result = round(float(model_answer), 1) == round(float(gt_answer), 1)
        return result
    except:
        return False


@hydra.main(version_base=None, config_path="config", config_name="test_model")
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
    
    dataset = load_dataset(
        "gsm8k",
        "main",
        split="train",
        cache_dir="/scr/jphilipp/tstar/datasets/gsm",
    )
    
    
    batch_prompts = []
    for i in range(args.n_prompts):
        batch_prompts.append([
            {"role": "user", "content": PROMPT.format(question=dataset['question'][i])}
        ])

    formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts
    ]
    
    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        max_new_tokens=2048,
        num_return_sequences=5, 
        best_of=5,
        temperature=1.0,
    )
    
    # format and write to json
    formatted_responses = [
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses
    ]
    
    extracted_responses = [extract_answer(response) for response in formatted_responses]
    gt_answers = [
    [round(float(gt_answer.split('####')[1].strip().lower().replace(",", "")), 1)] * args.n_shots 
    for gt_answer in dataset['answer'][:args.n_prompts]
    ]

    # Initialize a dictionary to hold the evaluation results
    evaluated_responses = {}

    # Iterate over each prompt and its corresponding ground truth answers
    for i in range(args.n_prompts):
        prompt_evaluations = []
        prompt_formatted_responses = []

        for shot in range(args.n_shots):
            model_answer = extracted_responses[i * args.n_shots + shot]
            gt = gt_answers[i][shot]
            evaluation = evaluate_model_response(model_answer, gt)
            prompt_evaluations.append(evaluation)
            prompt_formatted_responses.append(formatted_responses[i * args.n_shots + shot])
        
        evaluated_responses[i] = {
            "prompt_evaluations": prompt_evaluations,
            "formatted_responses": prompt_formatted_responses
        }

  
    breakpoint()
    
if __name__ == "__main__":
    fire.Fire(main())