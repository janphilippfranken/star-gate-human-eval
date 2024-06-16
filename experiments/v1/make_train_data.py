"""Generate generic responses without additional info or questions."""
import json
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
    with open(args.conversations, 'r') as f:
        conversations = json.load(f)
        
    # eig for best questions
    # with open(args.eig, 'r') as f:
    #    eig = json.load(f)
    
    # check whether this is a prompt that should involve follow-up
    # with open(args.eig, 'r') as f:
    #    eig = json.load(f)
    best_attempts = [1, 4, 5, 3, 4, 3, 4, 5, 6, 7]
    include_question =    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
        
    conversation_dict = {}
    for prompt_id, user_id, prompt, attempt, question, response in zip(*conversations.values()):
        conversation_key = f"prompt_{prompt_id}_user_{user_id}_attempt_{attempt}"
        conversation_dict[conversation_key] = {"prompt": prompt, "question": question, "response": response}   
    
    conversation_dict_filtered = {}
    
    for prompt_id in range(args.n_prompts):
        for user_id in range(args.n_users):
            key = f"prompt_{prompt_id}_user_{user_id}_attempt_{best_attempts[prompt_id]}"
            conversation_dict_filtered[key] = conversation_dict[key]
    
    # format prompts
    batch_prompts = []
    for i, (conversation_key, conversation) in enumerate(conversation_dict_filtered.items()):
        
        if include_question[i]: # if this is a prompt for which we should ask a question
            batch_prompts.append([
                {"role": "user", "content": conversation["prompt"]},
                {"role": "assistant", "content": conversation["question"]},
                {"role": "user", "content": conversation["response"]},
            ])
        
        else:  # if this is a prompt for which we should not ask a question
            batch_prompts.append([
                {"role": "user", "content": conversation["prompt"]},
            ])

    formatted_batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    
    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
        
    # format and write to json
    formatted_responses = [
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses
    ]
    
    # append final response to training data
    training_data = []
    for prompt, response in zip(batch_prompts, formatted_responses):
        training_data.append({"role": "assistant", "content": formatted_responses})
        
    # save as dataset with messages as key
    
    with open(args.save_file, 'w') as f:
        json.dump(training_data, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())