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



SYSTEM_PROMPT = """
You are an expert at generating diverse solutions to math problems and selecting the best one. You will first receive a problem and specific instructions from the user, then generate multiple unique solutions. Make sure to:

1. Use different methods for each solution attempt.
2. Use the special token `<|reserved_special_token_0|>` to mark the start and end of each attempt.
3. After completing all attempts, choose the best solution and provide it in the `<final_output>` tag.
"""

USER_PROMPT = """
Provide {N} step-by-step solutions to the following math problem. The last line of each solution should be of the form Answer: $ANSWER (without quotes) where $ANSWER is the answer to the problem.

{question}

Remember to put your answer on its own line after "Answer:", and you do not need to use a \boxed command. Each solution should be treated as one unique attempt.
"""

USER_EXAMPLE = """Provide 2 step-by-step solutions to the following math problem. The last line of each solution should be of the form Answer: $ANSWER (without quotes) where $ANSWER is the answer to the problem.\n\nEvaluate $\\left\\lceil3\\left(6-\\frac12\\right)\\right\\rceil$.\n\nRemember to put your answer on its own line after \"Answer:\", and you do not need to use a \boxed command. Each solution should be treated as one unique attempt."""

ASSISTANT_EXAMPLE = """<|reserved_special_token_0|>Attempt 1 Starts<|reserved_special_token_0|>\n\nTo evaluate the expression, we need to follow the order of operations, often remembered by the acronym PEMDAS: Parentheses, Exponents, Multiplication and Division (from left to right), Addition and Subtraction (from left to right).\n\nFirst, we evaluate the expression inside the parentheses: \n$6-\\frac{1}{2}$\n$= 6-0.5$\n$= 5.5$\n\nNow the expression becomes $\\left\\lceil 3(5.5) \\right\\rceil$.\n\nNext, we perform the multiplication:\n$3(5.5) = 16.5$\n\nNow the expression becomes $\\left\\lceil 16.5 \\right\\rceil$.\n\nFinally, the ceiling function $\\lceil x \\rceil$ rounds $x$ up to the nearest integer. So $\\lceil 16.5 \\rceil = 17$.\n\nAnswer: 17<|reserved_special_token_0|>Attempt 1 Ends<|reserved_special_token_0|>\n\n<|reserved_special_token_0|>Attempt 2 Starts<|reserved_special_token_0|>\n\nTo evaluate the given expression, we need to follow the order of operations (PEMDAS):\n\n1. Evaluate the expression inside the innermost parentheses: $6-\\frac{1}{2}$\n   This is equal to $6 - 0.5$, which is $5.5$\n\n2. Now we have $\\left\\lceil3(5.5)\\right\\rceil$\n3. Multiply $3$ and $5.5$: $3 \\times 5.5 = 16.5$\n\n4. Now we have $\\lceil 16.5 \\rceil$\n5. The ceiling function $\\lceil x \\rceil$ rounds a number up to the nearest integer. Since $16.5$ is between $16$ and $17$, it rounds up to $17$\n\nAnswer: 17<|reserved_special_token_0|>Attempt 2 Ends<|reserved_special_token_0|>\n\n<final_output>\nTo evaluate the given expression, we need to follow the order of operations (PEMDAS):\n\n1. Evaluate the expression inside the innermost parentheses: $6-\\frac{1}{2}$\n   This is equal to $6 - 0.5$, which is $5.5$\n\n2. Now we have $\\left\\lceil3(5.5)\\right\\rceil$\n3. Multiply $3$ and $5.5$: $3 \\times 5.5 = 16.5$\n\n4. Now we have $\\lceil 16.5 \\rceil$\n5. The ceiling function $\\lceil x \\rceil$ rounds a number up to the nearest integer. Since $16.5$ is between $16$ and $17$, it rounds up to $17$\n\nAnswer: 17\n</final_output>"""

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
    
    prompts = [USER_PROMPT.format(question=question, N=3) for question in problems[:args.end_prompts]]
    
    prompts = [
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_EXAMPLE},
            {"role": "assistant", "content": ASSISTANT_EXAMPLE},
            {"role": "user", "content": prompt}
        ]
        for prompt in prompts
    ]
    breakpoint()

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
            match = re.search(r"<final_output>([\s\S]*?)</final_output>", response)
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
    
    for i in indices:
        response = formatted_batch_responses[i]
        try:
            res = is_equiv(response, answer_strings[i]) 
            
            response_scores.append(int(res))
        except:
            response_scores.append(0)

    print(sum(response_scores)/len(response_scores))
if __name__ == "__main__":
    fire.Fire(main())