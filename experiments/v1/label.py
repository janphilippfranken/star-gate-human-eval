"""Generate responses without additional info or questions."""
import json
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *


PROMPT = """You are given a prompt that a user asked an assistant:

#### PROMPT STARTS
{prompt}
#### PROMPT ENDS

Your task is to determine whether this prompt is personal or not personal. A personal prompt means that the response should vary depending on the user's preferences and background. A not personal prompt means that the response should be the same for all users, regardless of their preferences and background.

Think step-by-step about whether a clarifying question is necessary to provide a personalized response. After your analysis, return 'Question Needed' if the prompt is personal and a clarifying question about the user's background and preferences is needed. If the prompt is not personal and no clarifying question is needed, return 'No Question Needed'.

Format your response as follows:
Reasoning: <your step-by-step reasoning>
Final Response: <your final response>"""


@hydra.main(version_base=None, config_path="config", config_name="respond")
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
    prompts = json.load(open('data/human_assistant_instruct.json', 'r'))

        
    # format prompts
    ids = []
    batch_prompts = []
    for i, prompt in enumerate(prompts[:100]):
        ids.append(i)
        batch_prompts.append([{"role": "user", "content": PROMPT.format(prompt=prompt)}])

    formatted_batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    
    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    breakpoint()
    
    # format and write to json
    formatted_responses = [
        response.split('<|end_header_id|>')[1].strip().split('Final Response:')[1].strip().split('\n\n')[0].strip()
        for response in batch_responses
    ]
    
    formatted_responses = [
        0 if formatted_response == 'No Question Needed' else 1 for formatted_response in formatted_responses
    ]
    
    with open('llama_labels.json', 'w') as f:
        json.dump(formatted_responses, f, indent=4)

if __name__ == "__main__":
    fire.Fire(main())