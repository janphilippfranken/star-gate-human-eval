"""Generate generic responses without additional info or questions."""
import os
import json
import copy
import torch
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="make_train_data")
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
    
    # conversations
    conversations = {k: [] for k in ['id', 'user_id', 'user', 'prompt', 'attempt', 'question', 'response']}
    for conversation_batch in sorted(os.listdir(args.conversations)):
        with open(f"{args.conversations}{conversation_batch}", 'r') as f:
            conversation_batch = json.load(f)
        for key in conversations:
            conversations[key].extend(conversation_batch[key])
        
    # eig for best questions
    best_question_attempts = []
    for eig_batch in sorted(os.listdir(args.eig)):
        with open(f"{args.eig}{eig_batch}", 'r') as f:
            eig_batch = json.load(f)
        eig_batch = [datum["best_question_idx_wo_pos_control"] for datum in eig_batch.values()]
        best_question_attempts.extend(eig_batch)
       
    with open(args.labels, 'r') as f:
       labels = json.load(f)
    
    conversation_dict = {}
    for prompt_id, user_id, user, prompt, attempt, question, response in zip(*conversations.values()):
        conversation_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
        conversation_dict[conversation_key] = {"prompt": prompt, "question": question, "response": response}
    
    # filter best attempts 
    conversation_dict_filtered = {}
    for prompt_id in range(args.n_prompts):
        
        best_attempt = best_question_attempts[prompt_id]
        print(prompt_id)
        prompt_attempt_users = [
                int(key.split("_")[3])
                for key in conversation_dict.keys()
                if int(key.split("_")[1]) == prompt_id and 
                int(key.split("_")[-1]) == best_attempt
            ]
        
        rand_user = prompt_attempt_users[0]
        # for user_id in prompt_attempt_users:
        key = f"prompt_{prompt_id}_user_{rand_user}_attempt_{best_attempt}"
        conversation_dict_filtered[key] = copy.deepcopy(conversation_dict[key])
    
    # format prompts
    batch_prompts = []
    batch_prompts_for_training = []
    for conversation_key, conversation in conversation_dict_filtered.items():
        prompt_key = int(conversation_key.split("_")[1])
        if True:
        # if labels[prompt_key] == 1: # if this is a prompt for which we should ask a question
            # now we dont want to include all of them because we have a bunch of them per user; so we only include 30% for now)
            batch_prompts.append([
                {"role": "user", "content": conversation["prompt"]},
                {"role": "assistant", "content": conversation["question"]},
                {"role": "user", "content": FINAL_RESPONSE_PROMPT.format(response=conversation["response"], question=conversation["question"], prompt=conversation["prompt"])},
            ])
            
            # batch_prompts.append([
            #     {"role": "user", "content": conversation["prompt"]},
            #     {"role": "assistant", "content": conversation["question"]},
            #     {"role": "user", "content": conversation["response"]},
            # ])
            
            batch_prompts_for_training.append([
                {"role": "user", "content": conversation["prompt"]},
                {"role": "assistant", "content": conversation["question"]},
                {"role": "user", "content": conversation["response"]},
            ])
        
        else:  # if this is a prompt for which we should not ask a question
            batch_prompts.append([{"role": "user", "content": conversation["prompt"]}])
            batch_prompts_for_training.append([{"role": "user", "content": conversation["prompt"]}])

    formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts
    ]
    
    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
        
    # format and write to json
    formatted_responses =  []
    for response in batch_responses:
        try:
            response = response.split('<|end_header_id|>')[1].strip()
            if "Final Response:" in response:
                response = response.split("Final Response:")[1].strip()
            formatted_responses.append(response)
        except:
            print(f"INVALID response: {response}")
            formatted_responses.append('<|invalid|>')

    # append final response to training data
    training_data = []
    for prompt, response in zip(batch_prompts_for_training, formatted_responses):
        conversation = prompt + [{"role": "assistant", "content": response}]
        training_data.append(conversation)
        
    # TODO: implement some filtering here if needed
    

    # save as dataset with messages as key
    with open(args.save_file, 'w') as f:
        json.dump(training_data, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())