"""Expected Info Gain Turn 2."""
import json
import fire
import hydra
import tqdm
import logging
import numpy as np
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from helpers import *
from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="expected_info_gain_turn_2")
def main(args: DictConfig) -> None:
    logging.info(f"""Computing EIG. Start Prompt: {args.prompt_start}. End Prompt: {args.prompt_end}
Saving to: {args.save_file}
Convo file: {args.conversations}
N_USER: {args.n_users_per_prompt}""")
   
    # model
    model = VLLMInferenceModel(
        **args.model_config
    )
    
    # tokenizer 
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=args.model_config.model,
        cache_dir=args.model_config.download_dir,
    )
    
    # gold responses
    with open(args.gold_responses, "r") as f:
        gold_responses = json.load(f)
       
    gold_responses = {
        f"{prompt_id}_{user_id}": gold_response for prompt_id, user_id, _, gold_response in
        zip(*gold_responses.values())
    }
        
    # conversations
    with open(args.conversations, "r") as f:
        conversations = json.load(f)
        
    conversation_dict = {}
    for prompt_id, user_id, prompt, attempt, question_turn_1, response_turn_1, question_turn_2, response_turn_2 in zip(*conversations.values()):
        conversation_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
        conversation_dict[conversation_key] = {
            "prompt": prompt, 
            "question_turn_1": question_turn_1, 
            "response_turn_1": response_turn_1,
            "question_turn_2": question_turn_2, 
            "response_turn_2": response_turn_2,
            }
  
    breakpoint()
    # logprobs container
    logprobs = {}

    # for prompt_id in tqdm.tqdm(set(conversations["id"])):
    for prompt_id in tqdm.tqdm(set(conversations["id"])):
        
        prompt_attempt_users = [
            int(key.split("_")[3])
            for key in conversation_dict.keys()
            if int(key.split("_")[1]) == prompt_id
        ]
        
        for i, user_id in enumerate(prompt_attempt_users): 
        
            for attempt in set(conversations["attempt"]):
                
                attempt_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"  
                
                logprobs[attempt_key] = []
                
                conversation_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
                gold_response_key = f"{prompt_id}_{user_id}"
                
                conversation = conversation_dict[conversation_key]
                gold_response = gold_responses[gold_response_key]

                
                prompt_without_response = [
                    {"role": "user", "content": conversation["prompt"]},
                    {"role": "assistant", "content": conversation["question_turn_1"]},
                    {"role": "user", "content": conversation["response_turn_1"]},
                    {"role": "assistant", "content": conversation["question_turn_2"]},
                    {"role": "user", "content": conversation["response_turn_2"]},
                    {"role": "assistant", "content": ""},
                ]
                
                prompt_with_response = [
                    {"role": "user", "content": conversation["prompt"]},
                    {"role": "assistant", "content": conversation["question_turn_1"]},
                    {"role": "user", "content": conversation["response_turn_1"]},
                    {"role": "assistant", "content": conversation["question_turn_2"]},
                    {"role": "user", "content": conversation["response_turn_2"]},
                    {"role": "assistant", "content": gold_response},
                ]              
    
                # format 
                formatted_prompt_without_response = tokenizer.apply_chat_template(prompt_without_response, tokenize=True)[:-1]
                formatted_prompt_with_response = tokenizer.apply_chat_template(prompt_with_response, tokenize=False)
                
                # breakpoint()
                outputs = model.prompt_logprobs(
                    prompts=[formatted_prompt_with_response],
                    n_logprobs_per_token=args.n_logprobs_per_token,
                )

                # get p_gold_given_conversation
                p_gold_given_conversation = outputs[0].prompt_logprobs[1 + len(formatted_prompt_without_response):] # type is dict so need to extract vals
                p_gold_given_conversation = [v.logprob for prob in p_gold_given_conversation for _, v in prob.items()]
            
                logprobs[attempt_key].append(np.mean(p_gold_given_conversation))
                
                # breakpoint()

    breakpoint()
    # now compute expected info gain
    eig = {}
    # magic needs to happen here ething else should be almost the same 
    for prompt_attempt_user_key, prompt_attempt_user_value in logprobs.items():
       
        if len(prompt_attempt_user_value) > 1: # softmax if we are longer than one 
            p_gold_given_prompt = torch.tensor(1/args.n_users_per_prompt).repeat(args.n_users_per_prompt) # baseline: uniform 
            p_gold_given_prompt_entropy = -(p_gold_given_prompt * torch.log(p_gold_given_prompt)).sum()
            p_gold_given_conversation = torch.softmax(torch.tensor(prompt_attempt_user_value), dim=0)
            p_gold_given_conversation_entropy = -(p_gold_given_conversation * torch.log(p_gold_given_conversation)).sum()
            eig[prompt_attempt_user_key] = (p_gold_given_prompt_entropy - p_gold_given_conversation_entropy).item()
            logging.info(eig[prompt_attempt_user_key])
        else:
            logging.info("ONE USER")
            eig[prompt_attempt_user_key] = prompt_attempt_user_value[0].item()
    
    best_questions = {}
    
    breakpoint()
    
    
    # prompts
    # users 
    # attemps 
    # each other user
    # each other users attempts 
    # for each prompt 
    for prompt_id in set(conversations["id"]):
        
        prompt_users = [
            int(key.split("_")[3])
            for key in conversation_dict.keys()
            if int(key.split("_")[1]) == prompt_id
        ]
        
        # we must find the best second turn question for each user 
        for i, user_id in enumerate(prompt_users):
            
            # so we loop over all attempts for that user 
            for attempt in set(conversations["attempt"]): 
                
                user_attempt_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"  
                
                # and then over all other users to compute expectation
                for j, other_user_id in enumerate(prompt_users):
                    
                    if j != i:
                        
                        for other_user_attempt in set(conversations["attempt"]):   
                            
                            other_user_attempt_key = f"prompt_{prompt_id}_user_{other_user_id}_attempt_{other_user_attempt}"  
                        
            
            

                best_question_eig_across_users.append(eig[attempt_key])
                best_question_responses.append(conversation_dict[attempt_key]["response_turn_2"])
                questions.append(conversation_dict[attempt_key]["question_turn_2"])
                users.append(user_id)
            
            # how much did this attempt help on average across users 
            best_question_indices.append(np.mean(best_question_eig_across_users))
            responses.append(best_question_responses)
       
        # best attempt across users
        best_question_idx = int(np.argmax(best_question_indices))
    
        # add this to our best questions for each prompt_id 
        best_questions[f"best_question_for_prompt_{prompt_id}"] = {}
        best_questions[f"best_question_for_prompt_{prompt_id}"]['question_performances'] = best_question_indices
        best_questions[f"best_question_for_prompt_{prompt_id}"]['questions'] = questions
        best_questions[f"best_question_for_prompt_{prompt_id}"]['responses'] = responses
        best_questions[f"best_question_for_prompt_{prompt_id}"]['best_question_idx'] = best_question_idx
        best_questions[f"best_question_for_prompt_{prompt_id}"]['best_question'] = questions[best_question_idx] 
        best_questions[f"best_question_for_prompt_{prompt_id}"]['best_response'] = responses[best_question_idx] 
        best_questions[f"best_question_for_prompt_{prompt_id}"]['user'] = users
   
        questions = []
        best_question_indices = []
        
        # breakpoint()

    with open(args.save_file, "w") as f:
        json.dump(best_questions, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())