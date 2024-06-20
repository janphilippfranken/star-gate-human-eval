import json
import fire
import hydra
import random
import numpy as np
from omegaconf import DictConfig
from tqdm import tqdm


from stargate.azure import AsyncAzureChatLLM
from stargate.gpt4 import GPT4Agent

from transformers import AutoTokenizer


SYSTEM_MESSAGE = """You are an expert in evaluating assistant responses, particularly skilled in analyzing their alignment with user backgrounds and preferences."""

GPT4_WIN_RATE = """For the following user query to an assistant, which of the assistant responses is more aligned with the user's background and preferences?

User Background: {user}

User Query: {query}

Assistant Response A: {response_a}

Assistant Response B: {response_b}

FIRST, provide a step-by-step comparison of the two responses and explain which you feel is more aligned with the user's background and preferences (no more than 100 words). 

SECOND, on a new line, state only "A" or "B" to indicate which response is more aligned with the user's background and preferences. 

Comparison: <step-by-step comparison and explanation>

Final Response: <"A" or "B">"""


from users import USER_21

@hydra.main(version_base=None, config_path="config", config_name="win_rates")
def main(args: DictConfig) -> None:
    
    responses_base_file = json.load(open('data/performance_5k_base.json'))
    breakpoint()
    responses_base = [r["response"] for r in responses_base_file.values()]
    responses_test_file = json.load(open('data/performance_5k_ckpt_2.json'))
    responses_test = [r["response"] for r in responses_test_file.values()]
    queries = [r["prompt"] for r in responses_test_file.values()]
    
    breakpoint()
    
    win_rates = []
  
    llm = AsyncAzureChatLLM(
        azure_endpoint="https://philipp.openai.azure.com/",
        api_version="2023-05-15",
    )
    
    model = GPT4Agent(
        llm=llm,
        model="gpt-4",
        temperature=0.0,
        top_p=0.9,
        max_tokens=200,
        n=1,
    )

    random.seed(1)

    prompts = []
    numbers = []
    breakpoint()
    
    for i, (response_base, response_test) in enumerate(zip(responses_base, responses_test)):
        
        rand_number = np.random.randint(2)
        numbers.append(rand_number)
        
        if rand_number == 0:
        
            prompt = GPT4_WIN_RATE.format(
                user=USER_21,
                query=queries[i],
                response_a=response_base,
                response_b=response_test,
            )
            prompts.append(prompt)
              
        elif rand_number == 1:
            prompt = GPT4_WIN_RATE.format(
                user=USER_21,
                query=queries[i],
                response_a=response_test,
                response_b=response_base,
                
            )
               
            prompts.append(prompt)
        
    responses = model.batch_prompt(
        system_message=SYSTEM_MESSAGE,
        messages=prompts,
        win_rates=True,
    )
    
    formatted_responses = []

    for response in responses:
        try:
            formatted_responses.append(response[0].split('Final Response:')[1].strip())
        except:
            formatted_responses.append("C")

    for formatted_response, number in zip(formatted_responses, numbers):
       
        if number == 0:

            if 'A' in formatted_response and 'B' not in formatted_response:
                win_rates.append((0))
                
            elif 'A' in formatted_response and 'B' in formatted_response:
                win_rates.append((0.5))
                
            elif 'A' not in formatted_response and 'B' in formatted_response:
                win_rates.append((1))
            else:
                print("ERROR")
                win_rates.append((0.5))
        
        elif number == 1:
            if 'A' in formatted_response and 'B' not in formatted_response:
                win_rates.append((1))
                
            elif 'A' in formatted_response and 'B' in formatted_response:
                win_rates.append((0.5))
                
            elif 'A' not in formatted_response and 'B' in formatted_response:
                win_rates.append((0))
            else:
                print("ERROR")
                win_rates.append((0.5))
                
    with open(f'data/win_rates-1e-5-epoch-2-250.json', 'w') as file:
        json.dump(win_rates, file, indent=4)
        
if __name__ == "__main__":
    fire.Fire(main())