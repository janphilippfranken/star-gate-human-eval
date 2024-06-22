"""Generate conversations with simulated users."""
import json
import fire
import torch
import hydra
import logging
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *
from helpers import get_formatted_responses

logging.basicConfig(level=logging.INFO)


@hydra.main(version_base=None, config_path="config", config_name="conversations")
def main(args: DictConfig) -> None:
    logging.info(f"""Generating Conversations. 
Start Prompt: {args.prompt_start}. 
End Prompt: {args.prompt_end}
Saving to: {args.save_file}
Seed: {args.seed}""")
    
    # seed
    torch.manual_seed(args.seed)
   
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
    
    # only keep up to max users used during training
    users = {
        k: v for k, v in users.items() 
        if int(k.split("_")[1]) < args.n_users
    }
    
    # STEP 1: questioner 
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
            logging.info(f"INVALID response: {response}")    
            formatted_batch_responses_questioner.append("<|invalid_response|>")
    
    
    


        
        
    
    # STEP 2: roleplayer 
    batch_prompts_roleplayer = []
    rand_user_ids = []
    n = args.generation_config_questioner.num_return_sequences
    
    for i, question in enumerate(formatted_batch_responses_questioner):
        
        prompt = prompts[i//n] 
        
        if i % n == 0:
            # randomly sample args.n_users_per_prompt each time we are at a new prompt
            rand_users = torch.randperm(args.n_users)[:args.n_users_per_prompt].tolist() # sample random users for this prompt 
        
        logging.info(rand_users)
        for rand_user_id in rand_users:
            
            user = users[f"user_{rand_user_id}"]
            rand_user_ids.append(rand_user_id)
            
            # random selection of max words for roleplayer 
            max_words = torch.normal(mean=args.roleplayer_mean_words, std=args.roleplayer_std_words, size=(1,))
            max_words = torch.clamp(max_words, args.roleplayer_min_words, args.roleplayer_max_words).int().item()
            
            # can either be bullet points or normal response
            rand_roleplay_prompt = torch.randint(len(ROLEPLAY_PROMPTS), (1,)).item()
            roleplay_prompt_key = list(ROLEPLAY_PROMPTS.keys())[rand_roleplay_prompt]
            
            batch_prompts_roleplayer.append([
                    {"role": "system", "content": f"You must adopt the following persona in all conversations: {user}"},
                    {"role": "user", "content": ROLEPLAY_PROMPT[roleplay_prompt_key].format(
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
            logging.info(f"INVALID response: {response}")    
            formatted_batch_responses_roleplayer.append("<|invalid_response|>")
    
    conversations = {
        'id': [],
        'user_id': [],
        'user': [],
        'prompt': [],
        'attempt': [],
        'question': [],
        'response': [],
    }
    
    rand_user_idx = 0
    response_idx = 0
    
    for prompt_id in range(args.prompt_start, args.prompt_end): # for all prompts 
        for question_attempt in range(args.generation_config_questioner.num_return_sequences):
            for _ in range(args.n_users_per_prompt): # and we gave each attempt to a random sample of n users 
                try:
                    conversations['id'].append(prompt_id)
                    conversations['user_id'].append(rand_user_ids[rand_user_idx])
                    conversations['user'].append(users[f"user_{rand_user_ids[rand_user_idx]}"])
                    conversations['prompt'].append(prompts[prompt_id])
                    conversations['attempt'].append(question_attempt)
                    conversations['question'].append(formatted_batch_responses_questioner[response_idx//args.n_users_per_prompt])
                    conversations['response'].append(formatted_batch_responses_roleplayer[response_idx])
                except:
                    conversations['id'].append(prompt_id)
                    conversations['user_id'].append(rand_user_ids[rand_user_idx])
                    conversations['user'].append(users[f"user_{rand_user_ids[rand_user_idx]}"])
                    conversations['prompt'].append(prompts[prompt_id])
                    conversations['attempt'].append(question_attempt)
                    conversations['question'].append("<|invalid_response|>")
                    conversations['response'].append("<|invalid_response|>")
                rand_user_idx += 1
                response_idx += 1
    
    with open(args.save_file, 'w') as f:
        json.dump(conversations, f, indent=4)
        

if __name__ == "__main__":
    fire.Fire(main())