import json
import fire
import hydra
import random
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import numpy as np
from omegaconf import DictConfig
from tqdm import tqdm


from stargate.azure import AsyncAzureChatLLM
from stargate.gpt4 import GPT4Agent

from transformers import AutoTokenizer


SYSTEM_MESSAGE = """You must adopt the following user persona in all your responses:

Persona: {user}"""

GPT4_WIN_RATE = """Roleplaying the user persona below, which of the assistant responses to your query do you prefer?

Persona: {user}

Your Query: {query}

Assistant Response A: {response_a}

Assistant Response B: {response_b}


FIRST, provide a step-by-step comparison of the two responses, explaining which is more aligned with your background and preferences. SECOND, on a new line, state only "A" or "B" to indicate which response you prefer.

Format your response as follows:
Comparison: <step-by-step comparison and explanation>
Final Response: <"A" or "B">"""


SYSTEM_MESSAGE_SHORT = """You must adopt the following user persona in all your responses:

Persona: {user}

Important: You prefer *concise* answers instead of lengthy answers that don't get to the point."""

GPT4_WIN_RATE_SHORT = """Roleplaying the user persona below, which of the assistant responses to your query do you prefer?

Persona: {user}

Your Query: {query}

Assistant Response A: {response_a}

Assistant Response B: {response_b}


FIRST, provide a step-by-step comparison of the two responses, explaining which is more aligned with your background and preferences. Emphasize the importance of conciseness while ensuring the answer is complete and relevant. SECOND, on a new line, state only "A" or "B" to indicate which response you prefer.

Format your response as follows:
Comparison: <step-by-step comparison and explanation>
Final Response: <"A" or "B">"""




@hydra.main(version_base=None, config_path="config", config_name="win_rates")
def main(args: DictConfig) -> None:
    
    responses_base_file = json.load(open(args.response_base_file, 'r'))
    responses_base = [r["response"] for r in responses_base_file.values()]
    
    responses_test_file = json.load(open(args.responses_test_file, 'r'))
    
    responses_test = [r["response"] for r in responses_test_file.values()]
    users = [r["user"] for r in responses_test_file.values()]

    queries = [r["prompt"] for r in responses_test_file.values()]
    
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
    
    for i, (response_base, response_test) in enumerate(zip(responses_base, responses_test)):
        
        rand_number = np.random.randint(2)
        numbers.append(rand_number)        
        rand_user = users[i]        
        
        if rand_number == 0:
        
            prompt = GPT4_WIN_RATE.format(
                user=rand_user,
                query=queries[i],
                response_a=response_base,
                response_b=response_test,
            )
            prompts.append(prompt)
              
        elif rand_number == 1:
            prompt = GPT4_WIN_RATE.format(
                user=rand_user,
                query=queries[i],
                response_a=response_test,
                response_b=response_base,
                
            )
               
            prompts.append(prompt)

    prompts = prompts
    if args.short_responses:
        responses = model.batch_prompt(
            system_message=SYSTEM_MESSAGE_SHORT,
            messages=prompts,
            win_rates=True,
        )
    else:
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
                    
    if args.short_responses:
        result_save_file = args.result_save_file.replace('.json', '_short.json')
        responses_save_file = args.responses_save_file.replace('.json', '_short.json')
    else:
        result_save_file = args.result_save_file
        responses_save_file = args.responses_save_file

    breakpoint()
    # logging.info(f"Saving win rates to: {result_save_file}")
    # with open(result_save_file, 'w') as file:
    #     json.dump(win_rates, file, indent=4)

    # # save responses
    # with open(responses_save_file, 'w') as file:
    #     json.dump(responses, file, indent=4)
        
if __name__ == "__main__":
    fire.Fire(main())