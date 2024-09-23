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


PROMPT = """
You are going to solve problems using multiple attempts. You will first receive specific problem instructions and the problem statement. Follow these steps:

1. Solve the problem using multiple attempts. Each attempt must be unique and diverse. Wrap each attempt in its own `<attempt>` tag, and surround all attempts within the `<attempts>` tag, as shown in the example below.
2. After completing all attempts, select the best one and wrap it in the `<best_attempt>` tag.

Important: You must follow the formatting example below when providing your output. Failure to do so will result in disqualification.

### Formatting Example:
Solve the problem below using 3 diverse attempts.

<problem>
The specific problem will be stated here.
</problem>

<attempts>
<|reserved_special_token_0|><attempt_1><|reserved_special_token_0|>
Step-by-step solution attempt 1 goes here.
Answer: 42
<|reserved_special_token_0|></attempt_1><|reserved_special_token_0|>

<|reserved_special_token_0|><attempt_2><|reserved_special_token_0|>
Step-by-step solution attempt 2 goes here.
Answer: 37
<|reserved_special_token_0|></attempt_2><|reserved_special_token_0|>

<|reserved_special_token_0|><attempt_3><|reserved_special_token_0|>
Step-by-step solution attempt 3 goes here.
Answer: 99
<|reserved_special_token_0|></attempt_3><|reserved_special_token_0|>
</attempts>

<best_attempt>
Your selected best attempt goes here.
Answer: 42
</best_attempt>

### Main Task:
Solve the problem below using {N} diverse attempts.

<problem>
Solve the following math problem step by step. The last line of each attempt should be of the form Answer: $ANSWER (without quotes) where $ANSWER is the answer to the problem.

{question}

Remember to put your answer on its own line after "Answer:", and you do not need to use a \\boxed command.
</problem>
"""


@hydra.main(version_base=None, config_path="config", config_name="evaluate_trained")
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
    
    prompts = [PROMPT.format(question=question, N=4) for question in problems[:args.end_prompts]]
    
    prompts = [
        [
            {"role": "system", "content": "You must follow the user instructions."},
            {"role": "user", "content": prompt}
        ]
        for prompt in prompts
    ]

    formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in prompts
    ]
    
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    
    breakpoint()
    # batch_responses = [
    #     response.split("<|start_header_id|>assistant<|end_header_id|>")[1].strip()
    #     for response in batch_responses   
    # ]
    
    best_answers = []
    for response in batch_responses:
        try:
            # Using a more flexible regex pattern to match content between tags
            match = re.search(r"<best_attempt>([\s\S]*?)</best_attempt>", response)
            if match:
                best_answers.append(match.group(1))
            else:
                best_answers.append("Null")
        except Exception as e:
            # Log the exception for debugging purposes
            best_answers.append("Null")
    
    breakpoint()

    formatted_batch_responses = []
    
    for response in best_answers:
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