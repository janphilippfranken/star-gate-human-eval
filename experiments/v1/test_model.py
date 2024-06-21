"""Generate generic responses without additional info or questions."""
import json
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

# from prompts import *
from users import *

ROLEPLAY_PROMPT = """You must adopt the following persona in all conversations: {user}

Roleplaying the above persona, answer the following question:

Question: What type of activities or settings do you usually enjoy on a date night, or are you open to trying something new and adventurous?

Format your response as follows:
Reasoning: <Your step-by-step reasoning reflecting on which attributes of your persona are most relevant to answering the above question. Repeat the key aspects of your persona relevant to the above question here in 3-5 sentences.>
Response: <Based on your reasoning and in no more than {max_words} words, provide a first-person response that directly addresses the question in a way that sounds natural coming from someone with your profile. Use "I" to refer to the above persona profile, focus on the most important aspects of your profile with respect to the question, and avoid repetition or hallucination. Do not use second-person or third-person pronouns in this section. Use bullet points only no full sentence here this needs to be a realistic human response. People are lazy! Remember, no more than {max_words} words!>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification. Remember: No more than {max_words} allowed. Also use lazy and weird response style like only bullet points etc no need for full sentences imagine being a lazy human user people are lazy people are lazy people are lazy people are lazy."""


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
    ids = []
    batch_prompts = []
    for i, prompt in enumerate(prompts[:5]):
        ids.append(i)
        batch_prompts.append([
            {"role": "user", "content": ROLEPLAY_PROMPT.format(user=USER_4, question=prompt, max_words=10)}
        ])

    formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts
    ]
    
    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts[:5],
        **args.generation_config,
    )
    
    # format and write to json
    formatted_responses = [
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses
    ]
    
    breakpoint()
if __name__ == "__main__":
    fire.Fire(main())