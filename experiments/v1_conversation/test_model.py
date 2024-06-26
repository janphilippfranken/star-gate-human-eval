"""Generate generic responses without additional info or questions."""
import json
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

# from prompts import *
from users import *

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
    with open(args.prompts, 'r') as f:
        prompts = json.load(f)
        
    # format prompts
    def prompt_model(batch_prompts, prompt):
                    
        batch_prompts.append(
            {"role": "user", "content": prompt}
        )

        formatted_batch_prompts = [
            tokenizer.apply_chat_template(prompt, tokenize=False) 
            for prompt in [batch_prompts]
        ]
        
        # get responses
        batch_responses = model.batch_prompt(
            prompts=formatted_batch_prompts,
            max_new_tokens=2048,
            num_return_sequences=1, 
            best_of=1,
            temperature=0.0,
        )
        
        # format and write to json
        formatted_responses = [
            response.split('<|end_header_id|>')[1].strip() 
            for 
            response in batch_responses
        ]
        batch_prompts.append(
            {"role": "assistant", "content": formatted_responses[0].strip()}
        )
        return formatted_responses[0], batch_prompts
    
    prompt = "When do I know whether my investment is good?"
    response, batch_prompts = prompt_model([], prompt)
    
    breakpoint()
if __name__ == "__main__":
    fire.Fire(main())