"""Generate generic responses without additional info or questions."""
import os
import json
import copy
import numpy as np
import fire
import hydra
import tqdm
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *

import logging


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
    
    # labels (whether to ask/not ask question)
    with open(args.labels, 'r') as f:
       labels = json.load(f)
    
    # conversations
    conversations = {k: [] for k in ['id', 'user_id', 'user', 'prompt', 'attempt', 'question', 'response']}
    for conversation_batch in sorted(os.listdir(args.conversations), key=lambda item: int(item.split("_")[2])):
        with open(f"{args.conversations}{conversation_batch}", 'r') as f:
            conversation_batch = json.load(f)
        for key in conversations:
            conversations[key].extend(conversation_batch[key])
            
    # conversation dict 
    conversation_dict = {}
    for prompt_id, user_id, user, prompt, attempt, question, response in zip(*conversations.values()):
        conversation_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
        conversation_dict[conversation_key] = {"prompt": prompt, "question": question, "response": response}
        
    # eig for best questions
    best_question_attempts = []
    for eig_batch in sorted(os.listdir(args.eig), key=lambda item: int(item.split("_")[2])):
        with open(f"{args.eig}{eig_batch}", 'r') as f:
            eig_batch = json.load(f)
        eig_batch = [datum["best_question_idx_wo_pos_control"] for datum in eig_batch.values()]
        best_question_attempts.extend(eig_batch)
    
    # filter best attempts based on eig 
    conversation_dict_filtered = {}
    rand_users = [] 
    # breakpoint()
    for prompt_id in range(args.start_prompts, args.end_prompts):
        best_attempt = best_question_attempts[prompt_id - args.start_prompts]
        logging.info(prompt_id)

        prompt_attempt_users = [
                int(key.split("_")[3])
                for key in conversation_dict.keys()
                if int(key.split("_")[1]) == prompt_id and 
                int(key.split("_")[-1]) == best_attempt
            ]
        
        rand_user = prompt_attempt_users[0] # just first user is rand user here because this was prev randomly sampled 
        rand_users.append(rand_user)
        
        key = f"prompt_{prompt_id}_user_{rand_user}_attempt_{best_attempt}"
        conversation_dict_filtered[key] = copy.deepcopy(conversation_dict[key])
        
        # breakpoint()
    
    # format prompts
    batch_prompts = []
    batch_prompts_for_training = []
    labels_int = [] # just a list of labels (1s or 0s)
    
    for conversation_key, conversation in conversation_dict_filtered.items():
        prompt_key = int(conversation_key.split("_")[1])

        labels_int.append(labels[prompt_key]) # we need t this later 
        if labels[prompt_key] == 1: # if this is a prompt for which we should ask a question
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
        
        else:  # if this is a prompt for which we should not ask a question we currently don't distill cot
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
        
    # format
    formatted_responses =  []
    for response in batch_responses:
        try:
            response = response.split('<|end_header_id|>')[1].strip()
            if "Final Personalized Response:" in response:
                response = response.split("Final Personalized Response:")[1].strip()
            formatted_responses.append(response)
        except:
            print(f"INVALID response: {response}")
            formatted_responses.append('<|invalid|>')
            
    if args.response_filtering:    
        # now need to load user to filter for p(user | x, response)
        users = json.load(open("data/users/users.json", "r"))
        n = args.generation_config.num_return_sequences
        # breakpoint()
        best_formatted_responses= []
        logprobs = {}
        
        for i, prompt in tqdm.tqdm(enumerate(batch_prompts_for_training)):
            
            logging.info(i)
            
            batch_responses = []
            logprobs[i] = [] # score the logprobs of the user for all batch resposnes 
            
            if labels_int[i] == 1: # if this was an item were we generated a question
            
                for j in range(i * n, (i + 1) * n):
                    
                    
                    prompt_without_response = [
                        {"role": "user", "content": USER_PREDICTION_PROMPT.format(prompt=prompt[0]["content"], response=formatted_responses[j])}
                    ]
                    
                    user_key = f"user_{rand_users[i]}"
                    
                    prompt_with_response = [
                        {"role": "user", "content": USER_PREDICTION_PROMPT.format(prompt=prompt[0]["content"], response=formatted_responses[j])},
                        {"role": "assistant", "content": f"User Profile: {users[user_key]}"},
                    ]
                    
                    batch_responses.append(formatted_responses[j])
                                    
                    # log probs
                    formatted_prompt_without_response = tokenizer.apply_chat_template(prompt_without_response, tokenize=True)
                    formatted_prompt_with_response = tokenizer.apply_chat_template(prompt_with_response, tokenize=False)
                            
                    outputs = model.prompt_logprobs(
                        prompts=[formatted_prompt_with_response],
                        n_logprobs_per_token=args.n_logprobs_per_token,
                    )

                    # get p_gold_given_conversation
                    p_user_given_conversation = outputs[0].prompt_logprobs[1 + len(formatted_prompt_without_response):] # type is dict so need to extract vals
                    p_user_given_conversation = [v for prob in p_user_given_conversation for _, v in prob.items()]
                    logprobs[i].append(np.mean(p_user_given_conversation))

                wrong_formats = [r for r in batch_responses if "Reasoning:" in r]
                corr_formats = []
                corr_formats_logprobs = []
                for r, logp in zip(batch_responses, logprobs[i]):
                    if r not in wrong_formats:
                        corr_formats.append(r)
                        corr_formats_logprobs.append(logp)
                
                best_response = corr_formats[np.argmax(corr_formats_logprobs)]
                print("len", len(corr_formats), len(corr_formats_logprobs))
                print(np.argmax(corr_formats_logprobs))
                best_formatted_responses.append(best_response)
            
                batch_responses = []

            else:
                best_formatted_responses.append(formatted_responses[i * n])
    else:
        print("Not Filtering.")
        best_formatted_responses = formatted_responses
        
    # append final response to training data
    training_data = []
    for prompt, response in zip(batch_prompts_for_training, best_formatted_responses):
        conversation = prompt + [{"role": "assistant", "content": response}]
        training_data.append(conversation)
    

    # save as dataset with messages as key
    with open(args.save_file, 'w') as f:
        json.dump(training_data, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())