"""Evaluate."""
import json
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer
from stargate.azure import AsyncAzureChatLLM
from stargate.gpt4 import GPT4Agent

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *

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


SYSTEM_PROMPT = """You are an expert at classifying prompts, highly skilled in determining whether an assistant has asked a clarifying question or provided a response."""

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
        prompts = json.load(f)[args.eval_prompt_start:args.eval_prompt_end]
             
    # format prompts
    ids = []
    batch_prompts = []
    for i, prompt in enumerate(prompts):
        ids.append(i + args.eval_prompt_start)
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
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses
    ]
    
    # now here comes the point where we need to see if model asked a follow-up question and go for it again
    breakpoint()
    formatted_gpt_prompts = [
        PROMPT.format(question=prompt, response=response) 
        for prompt, response in zip(prompts, formatted_responses)
    ]
    gpt_responses = gpt4.batch_prompt(system_message=SYSTEM_PROMPT, messages=formatted_gpt_prompts)
    formatted_gpt_responses = [int(resp[0].split('Final Response:')[1].strip()) for resp in gpt_responses]

    
    # now we prompt the model again with a random user, and then respond based on that to get a final response 
    batch_prompts = []
    for i, prompt in enumerate(prompts):
        ids.append(i + args.eval_prompt_start)
        batch_prompts.append([
            {"role": "user", "content": RESPONSE_PROMPT.format(question=prompt)}
        ])

    formatted_batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    
    
    labels = [1 if resp == "Question Needed" else 0 for resp in formatted_responses]
    
    breakpoint()
    
    with open(args.save_file, 'w') as f:
        json.dump(questioner_responses, f, indent=4)

if __name__ == "__main__":
    fire.Fire(main())