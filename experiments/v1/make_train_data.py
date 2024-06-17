"""Generate generic responses without additional info or questions."""
import json
import fire
import hydra
import torch
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
    with open(args.conversations, 'r') as f:
        conversations = json.load(f)
        
    # eig for best questions
    with open(args.eig, 'r') as f:
       eig = json.load(f)

    with open(args.labels, 'r') as f:
       labels = json.load(f)

    best_question_attempts = [
        datum["best_question_idx"] for datum in eig.values()
    ]
    
    conversation_dict = {}
    for prompt_id, user_id, prompt, attempt, question, response in zip(*conversations.values()):
        conversation_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
        conversation_dict[conversation_key] = {"prompt": prompt, "question": question, "response": response}   
    
    conversation_dict_filtered = {}
    
    for prompt_id in range(args.n_prompts):
        for user_id in range(args.n_users):
            key = f"prompt_{prompt_id}_user_{user_id}_attempt_{best_question_attempts[prompt_id]}"
            conversation_dict_filtered[key] = conversation_dict[key]

    # format prompts
    batch_prompts = []
    for conversation_key, conversation in conversation_dict_filtered.items():
        prompt_key = int(conversation_key.split("_")[1])
        if labels[prompt_key] == 1:# if this is a prompt for which we should ask a question
            batch_prompts.append([
                {"role": "user", "content": conversation["prompt"]},
                {"role": "assistant", "content": conversation["question"]},
                {"role": "user", "content": conversation["response"]},
            ])
        
        else:  # if this is a prompt for which we should not ask a question
            prompt = [{"role": "user", "content": conversation["prompt"]}]
            if prompt not in batch_prompts: # we only append once because we've already seen it! 
                batch_prompts.append(prompt)

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
            formatted_responses.append(response.split('<|end_header_id|>')[1].strip())
        except:
            print(f"INVALID response: {response}")
            formatted_responses.append('<|invalid|>')
            
    # append final response to training data
    training_data = []
    for prompt, response in zip(batch_prompts, formatted_responses):
        conversation = prompt + [{"role": "assistant", "content": response}]
        training_data.append(conversation)
        
    # TODO: implement some filtering here if needed
    
    breakpoint()
    # save as dataset with messages as key
    with open(args.save_file, 'w') as f:
        json.dump(training_data, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())