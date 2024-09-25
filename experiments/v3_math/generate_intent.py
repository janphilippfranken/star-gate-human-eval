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
You are an expert in generating diverse solutions to math problems and selecting the optimal one. Upon receiving a problem and specific instructions from the user, your tasks are to:

1. Create multiple unique solutions using different methods for each.
2. After completing all solutions, select the best one and enclose it within the `<final_output>` tags.
"""


@hydra.main(version_base=None, config_path="config", config_name="generate")
def main(args: DictConfig) -> None:
    
    torch.manual_seed(42)
    random.seed(42)
    
    logging.info(args)

    # model
    # model = VLLMInferenceModel(
    #     **args.model_config
    # )
    
    # # tokenizer 
    # tokenizer = AutoTokenizer.from_pretrained(
    #     pretrained_model_name_or_path=args.model_config.model,
    #     cache_dir=args.model_config.download_dir,
    # )
    
    # prompts
    dataset = load_dataset(
        "HannahRoseKirk/prism-alignment",
        "conversations",
        split="train",
        cache_dir="./data/prism",
    )
    feedback = dataset['open_feedback'][:100]
    conversations = dataset['conversation_history'][:100]
    filtered_feedback = []
    filtered_conversations = []
    opening_prompts = []
    for conversation, feedback in zip(conversations, feedback):
        try:
            filtered_conversation = ""
            for turn in conversation:
                if turn["role"] == "user":
                    filtered_conversation += f"\n\nUser: {turn['content'].strip()}"
                elif turn["role"] == "model":
                    if turn["if_chosen"] == True:
                        filtered_conversation += f"\n\nAssistant (chosen): {turn['content'].strip()}"
                    else:
                        filtered_conversation += f"\n\nAssistant (rejected): {turn['content'.strip()}"
                        
            
            filtered_conversation += f"\n\nFinal User Feedback: {feedback}"
            filtered_conversations.append(filtered_conversation)
            filtered_feedback.append(feedback)
            opening_prompts.append(conversation[0]["content"].strip())
        except:
            continue 
        
    breakpoint()
    
    
    
    
    
    
    breakpoint()
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

            N = random.randint(1, 8)
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