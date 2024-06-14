"""Generate responses without additional info or questions."""
import json
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="logprobs")
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
        
    # format prompts
    ids = []
    batch_prompts = []
    for user in [USER_1, USER_2, USER_3, USER_4, USER_5]:
        for i, (prompt, response) in enumerate(zip(prompts['prompt'][:args.n_prompts], prompts['response'][:args.n_prompts])):
            ids.append(i)

            batch_prompts.append([
                {"role": "user", "content": PROMPT_LOGPROBS.format(user=user, question=prompt[0]['content'])},
                {"role": "assistant", "content": response}
            ])

    formatted_batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    
    # get responses
    breakpoint()
    batch_logprobs = model.prompt_logprobs(
        prompts=formatted_batch_prompts,
        n_logprobs_per_token=args.n_logprobs_per_token,
    )
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
    )
    breakpoint()
    
    # format and write to json
    formatted_responses = [
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses
    ]
    
    questioner_responses = {
        'id': [],
        'prompt': [],
        'response': [],
    }
    
    for i, prompt, response in zip(ids, batch_prompts, formatted_responses):
        questioner_responses['id'].append(i)
        questioner_responses['prompt'].append(prompt)
        questioner_responses['response'].append(response)
    
    with open('base_introspection.json', 'w') as f:
        json.dump(questioner_responses, f, indent=4)

if __name__ == "__main__":
    fire.Fire(main())