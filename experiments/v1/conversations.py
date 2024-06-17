"""Generate conversations and filter good questions based on expected info gain."""
import json
import fire
import torch
import hydra
import logging
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="conversations")
def main(args: DictConfig) -> None:
    logging.info(f"Generating Conversations. Start Prompt: {args.prompt_start}. End Prompt: {args.prompt_end}")
   
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
    with open(args.prompts, 'r') as f:
        prompts = json.load(f)
                
    # users
    with open(args.users, 'r') as f:
        users = json.load(f)
    
    # QUESTIONER 
    batch_prompts_questioner = []
    for i in range(args.prompt_start, args.prompt_end):
        prompt = prompts[i]
        batch_prompts_questioner.append([
            {"role": "user", "content": QUESTION_PROMPT.format(question=prompt)}
        ])

    formatted_batch_prompts_questioner = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts_questioner]
    
    batch_responses_questioner = model.batch_prompt(
        prompts=formatted_batch_prompts_questioner,
        **args.generation_config_questioner,
    )

    formatted_batch_responses_questioner = []
    
    for response in batch_responses_questioner:
        try:
            formatted_batch_responses_questioner.append(response.split('Clarifying Question:')[1].strip())
        except:
            print(f"INVALID response: {response}")    
            formatted_batch_responses_questioner.append("<|invalid_response|>")
    
    # ROLEPLAYER 
    batch_prompts_roleplayer = []
    n = args.generation_config_questioner.num_return_sequences
    for user in enumerate(list(users.values())[:args.n_users]):
        for i, question in enumerate(formatted_batch_responses_questioner):
            prompt = prompts[i//n]
            
            # max words for roleplayer 
            max_words = torch.normal(mean=args.roleplayer_mean_words, std=args.roleplayer_std_words, size=(1,))
            max_words = torch.clamp(max_words, args.roleplayer_min_words, args.roleplayer_max_words).int().item()
            
            batch_prompts_roleplayer.append([
                    {"role": "system", "content": f"You must adopt the following persona in all conversations: {user}"},
                    {"role": "user", "content": ROLEPLAY_PROMPT.format(
                        user=user, 
                        question=question, 
                        max_words=max_words,
                )}
            ])

    formatted_batch_prompts_roleplayer = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts_roleplayer]
    
    batch_responses_roleplayer = model.batch_prompt(
        prompts=formatted_batch_prompts_roleplayer,
        **args.generation_config_roleplayer,
    )
    

    formatted_batch_responses_roleplayer = []
    for response in batch_responses_roleplayer:
        try:
            formatted_batch_responses_roleplayer.append(response.split('Response:')[1].strip().strip('"'))
        except:
            print(f"INVALID response: {response}")    
            formatted_batch_responses_roleplayer.append("<|invalid_response|>")
    
    conversations = {
        'id': [],
        'user': [],
        'prompt': [],
        'attempt': [],
        'question': [],
        'response': [],
    }
    
    response_idx = 0
    for user_id in range(args.n_users):
        question_idx = 0
        for prompt_id in range(args.prompt_start, args.prompt_end):
            for question_attempt in range(args.generation_config_questioner.num_return_sequences):
                try:
                    conversations['id'].append(prompt_id)
                    conversations['user'].append(user_id)
                    conversations['prompt'].append(prompts[prompt_id])
                    conversations['attempt'].append(question_attempt)
                    conversations['question'].append(formatted_batch_responses_questioner[question_idx])
                    conversations['response'].append(formatted_batch_responses_roleplayer[response_idx])
                except:
                    print(f"INVALID: {prompt_id} and {user_id}")
                    conversations['id'].append(prompt_id)
                    conversations['user'].append(user_id)
                    conversations['prompt'].append(prompts[prompt_id])
                    conversations['attempt'].append(question_attempt)
                    conversations['question'].append("<|invalid_response|>")
                    conversations['response'].append("<|invalid_response|>")
                question_idx += 1
                response_idx += 1
    
    with open(args.save_file, 'w') as f:
        json.dump(conversations, f, indent=4)
        

if __name__ == "__main__":
    fire.Fire(main())