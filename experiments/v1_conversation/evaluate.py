"""Evaluate."""
import json
import fire
import hydra
import numpy as np
from omegaconf import DictConfig
from transformers import AutoTokenizer
from stargate.azure import AsyncAzureChatLLM
from stargate.gpt4 import GPT4Agent

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *


from users import USER_21

# gpt 4 agent
llm = AsyncAzureChatLLM(
    azure_endpoint="https://philipp.openai.azure.com/",
    api_version="2023-05-15",
)

gpt4 = GPT4Agent(
    llm=llm,
    model="gpt-4",
    temperature=0.0,
    top_p=0.9,
    max_tokens=200,
    n=1,
)


SYSTEM_PROMPT = """You are an expert at classifying prompts, highly skilled in determining whether an assistant has asked a clarifying question or answered directly."""

PROMPT = """You are given a question that a user asked the assistant and the assistant's response:

User Question: {question}

Assistant Response: {response}

Your task is to determine whether the assistant's response is a 'Clarifying Question' or an 'Answer' based on the following definitions:

Definition of Clarifying Question: A clarifying question is a query posed to gain a better understanding of a statement, instruction, or situation. It aims to eliminate ambiguity and ensure clear and accurate communication.

Definition of Answer: An answer is a reply or reaction to a question, statement, or situation. It provides information, feedback, or an answer to what has been communicated.

Format your response as follows:

Reasoning: <your step-by-step reasoning determining whether the 'Assistant Response' better aligns with the definition of 'Clarifying Question' or 'Answer'. Provide a justification for your choice.>
Final Response: <state only 1 if the response is a clarifying question, or 0 if it is an answer, and nothing else.>"""





@hydra.main(version_base=None, config_path="config", config_name="evaluate")
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
        prompts = json.load(f)[:200]
        
    # prompts = [datum['question'] for datum in prompts]
    breakpoint()
             
    # format prompts for initial query 
    ids = []
    batch_prompts = []
    for i, prompt in enumerate(prompts):
        ids.append(i)
        batch_prompts.append([
            {"role": "user", "content": RESPONSE_PROMPT.format(question=prompt)}
        ])

    formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) 
        for prompt in batch_prompts
    ]
    
    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )

    # format 
    formatted_responses = [
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses
    ]
    
    # now we need to call GPT to check if response includes question
    formatted_gpt_prompts = [
        PROMPT.format(question=prompt, response=response) 
        for prompt, response in zip(prompts, formatted_responses)
    ]

    gpt_responses = gpt4.batch_prompt(system_message=SYSTEM_PROMPT, messages=formatted_gpt_prompts)
    
    formatted_gpt_responses = [
        int(resp[0].split('Final Response:')[1].strip()) 
        for resp in gpt_responses
    ]
    
    # load the OG labels to compute agreement between gpt4 and model asked questions
    breakpoint()
    labels_human = json.load(open('data/labels/exp_when_9_pp_maj_votes_0_200.json'))
    agreement = np.mean([i == j for i, j in zip(labels_human, formatted_gpt_responses) if i == 0])
    print("AGREEMENT", agreement)
    breakpoint()
    
    # now back to prompting roleplayer 
    batch_prompts_roleplayer = []
    for i, prompt in enumerate(prompts):
        if int(formatted_gpt_responses[i]) == 1:
            batch_prompts_roleplayer.append([
                    {"role": "system", "content": f"You must adopt the following persona in all conversations: {USER_21}"},
                    {"role": "user", "content": ROLEPLAY_PROMPT.format(
                        user=USER_21, 
                        question=formatted_responses[i].strip(),
                        max_words=20,
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
            formatted_batch_responses_roleplayer.append(response.split('Response:')[1].strip().strip('"'))
        except:
            print(f"INVALID response: {response}")    
            formatted_batch_responses_roleplayer.append("<|invalid_response|>")
            
    breakpoint()
    
    breakpoint()
    
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
            }
            f_counter += 1
        else:
            final_performance[i] = {
                'prompt': prompt,
                'response': formatted_responses[i],
            }
    breakpoint()
    
    labels = [1 if resp == "Question Needed" else 0 for resp in formatted_responses]
    # get win rates too for one held out user here 
    breakpoint()
    
    with open('results/not-cot-distilled-ckpt-2.json', 'w') as f:
        json.dump(final_performance, f, indent=4)

if __name__ == "__main__":
    fire.Fire(main())