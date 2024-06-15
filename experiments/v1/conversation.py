"""Generate conversations and filter good questions based on expected info gain."""
import json
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="conversation")
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
    
    # prompts
    with open(args.prompts, 'r') as f:
        prompts = json.load(f)
                
    # TODO: multiturn 
    
    # QUESTIONER 
    batch_prompts_questioner = []
    for i, prompt in enumerate(prompts[:args.n_prompts]):
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
    
    formatted_batch_responses_questioner = [
        response.split('Clarifying Question:')[1].strip()
        for response in batch_responses_questioner
    ]
    
    # ROLEPLAYER 
    batch_prompts_roleplayer = []
    n = args.generation_config_questioner.num_return_sequences
    for user in [USER_1, USER_2, USER_3, USER_4, USER_5]:
        for i, question in enumerate(formatted_batch_responses_questioner):
            prompt = prompts[i//n]
            batch_prompts_roleplayer.append([
                    {"role": "system", "content": f"You must adopt the following persona in all conversations: {user}"},
                    {"role": "user", "content": ROLEPLAY_PROMPT.format(
                        user=user, 
                        question=question, 
                        max_words=args.roleplayer_max_words,
                )}
            ])

    formatted_batch_prompts_roleplayer = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts_roleplayer]
    
    batch_responses_roleplayer = model.batch_prompt(
        prompts=formatted_batch_prompts_roleplayer,
        **args.generation_config_roleplayer,
    )

    formatted_batch_responses_roleplayer = [
        response.split('Response:')[1].strip().strip('"')
        for response in batch_responses_roleplayer
    ]
    
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
        for prompt_id in range(args.n_prompts):
            for question_attempt in range(args.generation_config_questioner.num_return_sequences):
                conversations['id'].append(prompt_id)
                conversations['user'].append(user_id)
                conversations['prompt'].append(prompts[prompt_id])
                conversations['attempt'].append(question_attempt)
                conversations['question'].append(formatted_batch_responses_questioner[question_idx])
                conversations['response'].append(formatted_batch_responses_roleplayer[response_idx])
                question_idx += 1
                response_idx += 1
    
    with open('data/conversations.json', 'w') as f:
        json.dump(conversations, f, indent=4)

if __name__ == "__main__":
    fire.Fire(main())