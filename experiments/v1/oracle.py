import json
import fire
import random
import hydra
import re
import numpy as np
import os
from omegaconf import DictConfig
from tqdm import tqdm
import torch
from datasets import load_dataset
from stargate.vllm_inference_model import VLLMInferenceModel
from transformers import AutoTokenizer



N_ITEMS = 2000
CoT = False

PROMPT_INSTRUCT = """Respond to the query below. Format your answer as follows:

Q: <query here>
A: <your final answer here>

Q: {question}"""


def format_response(response):
    formatted_response = ""
    try:
        formatted_response = response.split("A:")[1].strip().lower()
    except:
        print("invalid, continue")
    return formatted_response

def extract_answer(answer):
    if '=' in answer:
        answer = answer.split('=')[-1].strip()
    answer = answer.replace(",", "")
    try:
        answer = re.findall(r"\d+", answer.strip())[-1]
        answer = int(answer)
    except:
        answer = "[invalid]"
    return answer

def evaluate_model_response(model_answer, gt_answer):
    try:
        result = int(model_answer) == int(gt_answer)
        return result
    except:
        return False


# main evaluation script
@hydra.main(version_base=None, config_path="config", config_name="oracle")
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
    # breakpoint()
    batch_prompts = ["""Turn 1:
A: Did you catch the soccer match last night? Our team played incredibly well!
B: Yeah, it was an amazing game! We really deserved that win. By the way, I just got off the call with the client. They are really unhappy with the final deliverable.
A: Oh no, what did they say specifically?
Turn 2:
B: They mentioned that the design is not user-friendly and the functionality is lacking in several key areas.
A: That's really disappointing. We spent so much time making sure everything was perfect. I know, but looking back, I think we missed some crucial user feedback during the testing phase.
B: True, but we did get some positive comments from the initial focus group. Maybe we can build on that feedback.
Turn 3:
A: Yeah, but considering the overall response, I feel like we didn't prioritize the right features. Honestly, after hearing their feedback, I can't help but think, "we deserve to lose after that."
B: It's tough to hear, but we can learn from this and make sure it doesn't happen again. Let's regroup and come up with a solid plan. In the meantime, why don't we grab drinks tonight? I think we could both use a break after this.
A: That sounds great! A little relaxation might help us come back to this with fresh eyes tomorrow. is the statement ' we deserve to lose after that' positive, negative, or neutral? answer in one word"""]
    batch_prompts = [[{"role" : "user", "content": prompt}] for prompt in batch_prompts]
    batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    breakpoint()
    batch_responses = model.batch_prompt(
        prompts=batch_prompts,
        **args.generation_config,
    )
  

if __name__ == "__main__":
    fire.Fire(main())