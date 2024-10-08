"""Evaluate."""
import json
import fire
import hydra
import random
import torch
import logging
import numpy as np
from omegaconf import DictConfig
from transformers import AutoTokenizer, AutoModelForCausalLM
from stargate.azure import AsyncAzureChatLLM
from stargate.gpt4 import GPT4Agent

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *

# from users import *


# gpt 4 agent
llm = AsyncAzureChatLLM(
        azure_endpoint="https://philipp.openai.azure.com/",
        api_version="2024-07-01-preview",
    )

gpt4 = GPT4Agent(
    llm=llm,
    model="gpt-4o",
    temperature=0.0,
    top_p=0.9,
    max_tokens=500,
    n=1,
)


SYSTEM_PROMPT = """You are an expert at classifying prompts, highly skilled in determining whether an assistant has asked a clarifying question or provided a direct answer."""

PROMPT = """You are given a user's question to the assistant and the assistant's response:

User Question: {question}

Assistant Response: {response}

Your task is to determine whether the assistant's response is a 'Clarifying Question' or a 'Direct Answer' based on the following definitions:

Definition of Clarifying Question: A clarifying question is a query posed to gain a better understanding of a statement, instruction, or situation. It aims to eliminate ambiguity, ensure clear and accurate communication, and may ask for the user's background or personal information to provide a more tailored response.

Definition of Direct Answer: A direct answer is a reply that directly addresses the user's question without asking for additional information first.

Format your response as follows:

Reasoning: <Provide your step-by-step reasoning for determining whether the 'Assistant Response' aligns more closely with the definition of 'Clarifying Question' or 'Direct Answer'. Justify your choice.>
Final Response: <State only '1' if the response is a clarifying question, or '0' if it is a direct answer, and nothing else.>"""


QUESTION_SYSTEM_PROMPT = """You are an AI assistant. For each user query:

1. Carefully analyze the query and any provided context.

2. Decide whether to answer directly or ask a clarifying question:

   Answer Directly when:
   - A response based on general knowledge would satisfy the query.
   - Additional personal information wouldn't significantly improve your answer.
   - Example: "What are the three laws of motion?"

   Ask a Clarifying Question when:
   - Knowing more about the user's situation would result in a noticeably better answer.
   - A tailored response would be more valuable than a generic one.
   - Example: "I have a 3-day weekend coming up. What should I do?"

3. Based on your decision:
   - If answering directly, provide a comprehensive response using available information.
   - If clarifying, ask ONE clear, concise question directly related to the query.

4. After a follow-up (if asked), give a final, thorough response.

Aim to provide the most helpful interaction for each specific query.
"""


@hydra.main(version_base=None, config_path="config", config_name="evaluate")
def main(args: DictConfig) -> None:
    
    random.seed(1)
   
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
        prompts = json.load(f)[:args.n_prompts]        
            
    # users
    users_raw = json.load(open(args.users))
    users = {}
    for user_id, info in users_raw.items():
        if int(user_id.split('_')[-1]) >= args.user_start:
            users[user_id] = info
        
    # format prompts for initial query 
    ids = []
    batch_prompts = []
    for i, prompt in enumerate(prompts):
        ids.append(i)
        if args.use_question_system:
            if i == 0:
                logging.info("Using question system prompt")
            batch_prompts.append([
                {"role": "system", "content": QUESTION_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ])
        else:
            if i == 0:
                logging.info("Do not use question system prompt")
            batch_prompts.append([
                {"role": "user", "content": prompt}
            ])

    formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts
    ]    
    # """ Prompt hugginf face model """
    # pretrained_model_name_or_path = args.model_config.model
    # cache_dir = args.model_config.download_dir    
    # hg_model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path=pretrained_model_name_or_path, cache_dir=cache_dir, torch_dtype=torch.bfloat16, device_map='auto')
    # from transformers import pipeline
    # text_gen = pipeline('text-generation', model=hg_model, tokenizer=tokenizer)
    # """ Prompt hugginf face model """    

    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    
    # format 
    formatted_responses = [
        response.split('<|end_header_id|>')[-1].lstrip().strip()
        for response in batch_responses
    ]    

    # now we need to call GPT to check if response includes question
    formatted_gpt_prompts = [
        PROMPT.format(question=prompt, response=response) 
        for prompt, response in zip(prompts, formatted_responses)
    ]
    
    gpt_responses = gpt4.batch_prompt(system_message=SYSTEM_PROMPT, messages=formatted_gpt_prompts)
    
    formatted_gpt_responses = []
    n_errors = 0
    for i, resp in enumerate(gpt_responses):
        try:
            formatted_gpt_responses.append(int(resp[0].split('Final Response:')[1].strip()))
        except:
            print(f"Error in response {i}")
            # print(resp)
            n_errors += 1
            formatted_gpt_responses.append(0)
    
    logging.info(f"Number of errors: {n_errors}")
    # formatted_gpt_responses = [
    #     int(resp[0].split('Final Response:')[1].strip()) 
    #     for resp in gpt_responses
    # ]
    
    # load the OG labels to compute agreement between gpt4 and model asked questions    
    labels_human = json.load(open('data/labels/exp_when_9_pp_maj_votes_0_200.json'))
    agreement = np.mean([i == j for i, j in zip(labels_human, formatted_gpt_responses)])
    print("AGREEMENT", agreement)
        
    # now back to prompting roleplayer 
    batch_prompts_roleplayer = []
    rand_users = []
    for i, prompt in enumerate(prompts):
        rand_user = random.choice(list(users.keys()))
        # @TODO: currently using user 21 for all prompts        
        rand_user = users['user_21']
        rand_users.append(rand_user)        
        if int(formatted_gpt_responses[i]) == 1:
            max_words = torch.normal(mean=args.roleplayer_mean_words, std=args.roleplayer_std_words, size=(1,))
            max_words = torch.clamp(max_words, args.roleplayer_min_words, args.roleplayer_max_words).int().item()            
            batch_prompts_roleplayer.append([
                    {"role": "system", "content": f"You must adopt the following persona in all conversations: {rand_user}"},
                    {"role": "user", "content": ROLEPLAY_PROMPT.format(
                        max_words=max_words,
                        prompt=prompt,
                        question=formatted_responses[i].strip(),                        
                )}
            ])

    formatted_batch_prompts_roleplayer = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts_roleplayer
    ]
    
    batch_responses_roleplayer = model.batch_prompt(
        prompts=formatted_batch_prompts_roleplayer,
        **args.generation_config,
    )

    # format and write to json
    formatted_responses_roleplayer = [
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses_roleplayer
    ]
    
    formatted_batch_responses_roleplayer = []
    for response in formatted_responses_roleplayer:
        try:
            if 'Response:' in response:
                formatted_batch_responses_roleplayer.append(response.split('Response:')[1].strip().strip('"'))
            else:
                formatted_batch_responses_roleplayer.append(response.strip().strip('"'))
        except:
            print(f"INVALID response: {response}")    
            formatted_batch_responses_roleplayer.append("<|invalid_response|>")                
    
    batch_prompts_final = []
    response_count = 0
    for i, prompt in enumerate(prompts):
        if int(formatted_gpt_responses[i]) == 1:
            batch_prompts_final.append([
                {"role": "user", "content": prompts[i]},
                {"role": "assistant", "content": formatted_responses[i]},
                {"role": "user", "content": formatted_batch_responses_roleplayer[response_count]}
            ])
            response_count += 1
    
    formatted_batch_prompts_final = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts_final 
    ]
    
    batch_responses_final = model.batch_prompt(
        prompts=formatted_batch_prompts_final ,
        **args.generation_config,
    )
    
    formatted_responses_final = [
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses_final
    ]
    
    final_performance = {}
    f_counter = 0
    for i, prompt in enumerate(prompts):
        final_performance[i] = {}
        if int(formatted_gpt_responses[i]) == 1:
            final_performance[i] = {
                'prompt': prompt,
                'question': formatted_responses[i],
                'response': formatted_responses_final[f_counter],
                'roleplayer': formatted_batch_responses_roleplayer[f_counter],                
                'user': rand_users[i]
            }
            f_counter += 1
        else:
            final_performance[i] = {
                'prompt': prompt,
                'response': formatted_responses[i],
                'user': rand_users[i]
            }
    
    with open(args.save_responses, 'w') as f:
        json.dump(final_performance, f, indent=4)
        
    with open(args.save_questions, 'w') as f:
        json.dump(formatted_gpt_responses, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main())