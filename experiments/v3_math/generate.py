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

ASSISTANT_PROMPT = """
{attempts}

<final_output>
{best_attempt}
</final_output>
"""

PROMPT = """Solve the following math problem step by step. The last line of your response should be of the form Answer: $ANSWER (without quotes) where $ANSWER is the answer to the problem. 

{question}

Remember to put your answer on its own line after "Answer:", and you do not need to use a \\boxed command."""


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
        "hendrycks/competition_math",
        split="train",
        cache_dir="./data/math",
    )
    
    problems = [datum["problem"] for datum in dataset]
    solutions = [datum["solution"] for datum in dataset]
    answer_strings = [remove_boxed(last_boxed_only_string(solution)) for solution in solutions]
    
    prompts = [PROMPT.format(question=question) for question in problems[:args.end_prompts]]
    
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
                answer = response.split("\n\nAnswer:")[1].strip()
                res = is_equiv(answer, answer_strings[i]) 
                response_scores[i].append(int(res))
            except:
                response_scores[i].append(0)
                
    with open(args.save_file_scores, "w") as f:
        json.dump(response_scores, f, indent=4)
    
    with open(args.save_file_responses, "w") as f:
        json.dump(formatted_batch_responses, f, indent=4)
        
    train_data = []
    correct_attempts = []
    
    for i in range(args.end_prompts):
        if sum(response_scores[i]) == 0:
            continue
        try: 
            answers = [response.split("\n\nAnswer:")[1].strip() for response in formatted_batch_responses[i]]
            correct_indices = [k for k, score in enumerate(response_scores[i]) if score == 1]
            
            correct_response_idx = random.choice(correct_indices)
            correct_response = formatted_batch_responses[i].pop(correct_response_idx)

            N = random.randint(1, args.n_return)
            shown_responses = formatted_batch_responses[i][:N - 1] + [correct_response]
            random.shuffle(shown_responses)
            
            responses = "\n\n".join(
                [f"<|reserved_special_token_0|>Attempt {j + 1} Starts<|reserved_special_token_0|>\n\n{shown_response}<|reserved_special_token_0|>Attempt {j + 1} Ends<|reserved_special_token_0|>" for j, shown_response in enumerate(shown_responses)]
            ).strip()
            
            answers = [response.split("\n\nAnswer:")[1].strip() for response in shown_responses]
            results = [int(is_equiv(answer, answer_strings[i])) for answer in answers]
            
            train_data.append([
                {"role": "system", "content": f"{SYSTEM_PROMPT.strip()}"},
                {"role": "user", "content": f"{USER_PROMPT.format(question=problems[i], N=N).strip()}"},
                {"role": "assistant", "content": ASSISTANT_PROMPT.format(attempts=responses, best_attempt=correct_response).strip()},
            ])
            
            correct_attempts.append(results)
            
        except:
            continue 
    
    with open(args.save_train_responses, "w") as f:
        json.dump(train_data, f, indent=4)
        
    with open(args.save_train_labels, "w") as f:
        json.dump(correct_attempts, f, indent=4)
                
if __name__ == "__main__":
    fire.Fire(main())