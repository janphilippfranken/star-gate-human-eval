"""Generate generic responses without additional info or questions."""
import json
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="base_responses")
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
    with open(args.prompts, "r") as f:
        prompts = json.load(f)
        
    # format prompts
    ids = []
    batch_prompts = []
    for i, prompt in enumerate(prompts[:args.n_prompts]):
        ids.append(i)
        batch_prompts.append([
            {"role": "user", "content": RESPONSE_PROMPT.format(question=prompt)}
        ])

    formatted_batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    
    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    
    # format and write to json
    formatted_responses = [
        response.split("<|end_header_id|>")[1].strip() 
        for response in batch_responses
    ]
    
    questioner_responses = {
        "prompt_id": [],
        "prompt": [],
        "response": [],
    }
    
    for i, prompt, response in zip(ids, prompts, formatted_responses):
        questioner_responses["prompt_id"].append(i)
        questioner_responses["prompt"].append(prompt)
        questioner_responses["response"].append(response)
    
    with open(args.save_file, "w") as f:
        json.dump(questioner_responses, f, indent=4)

if __name__ == "__main__":
    fire.Fire(main())