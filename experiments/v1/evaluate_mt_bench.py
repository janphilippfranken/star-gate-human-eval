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

def load_prompts(question_file: str):
    """Load questions from a file."""
    questions = []
    with open(question_file, "r") as ques_file:
        for line in ques_file:
            if line:
                questions.append(json.loads(line))
    return questions


GPT4_SYSTEM_MESSAGE = "You are an expert at evaluating AI assistant responses."

GPT$_MT_GRADING_PROMPT = """Please act as an impartial judge and evaluate the quality of the responses provided by two AI assistants to the user question displayed below. You should choose the assistant that follows the user's instructions and answers the user's question better. Your evaluation should consider factors such as the helpfulness, relevance, accuracy, depth, creativity, and level of detail of their responses. Begin your evaluation by comparing the two responses and provide a short explanation. Avoid any position biases and ensure that the order in which the responses were presented does not influence your decision. Do not allow the length of the responses to influence your evaluation. Do not favor certain names of the assistants. Be as objective as possible. After providing your explanation, output your final verdict by strictly following this format: "[[A]]" if assistant A is better, "[[B]]" if assistant B is better, and "[[C]]" for a tie.

[User Question]
{question}

[The Start of Assistant A's Answer]
{answer_a}
[The End of Assistant A's Answer]

[The Start of Assistant B's Answer]
{answer_b}
[The End of Assistant B's Answer]

Format your response as follows:
Reasoning: <your step-by-step reasoning evaluating each response>
Final Response: <state only "[[A]]" if assistant A is better, "[[B]]" if assistant B is better, and "[[C]]" for a tie>"""



@hydra.main(version_base=None, config_path="config", config_name="evaluate_mt_bench")
def main(args: DictConfig) -> None:
   
    # model
    model_base = VLLMInferenceModel(
        **args.model_config_base
    )
    
    model_test = VLLMInferenceModel(
        **args.model_config_test
    )
    
    # tokenizer 
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=args.model_config.model,
        cache_dir=args.model_config.download_dir,
    )
    
    # prompts
    prompts = load_prompts(args.prompts)
             
    # format prompts
    batch_prompts = []
    for prompt in tqdm(prompts, desc="Processing Prompts"):
        batch_prompts.append([
            {"role": "user", "content": prompt}
        ])
        
    formatted_batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    
    # get responses
    batch_responses_base = model_base.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    
    batch_responses_test = model_test.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    
    # format and write to json
    formatted_responses_base = [
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses_base
    ]
    
    formatted_responses_test = [
        response.split('<|end_header_id|>')[1].strip() 
        for response in batch_responses_test
    ]
    
    # now here comes the point where we need to see if model asked a follow-up question and go for it again
    breakpoint()
    formatted_gpt_prompts = [
        PROMPT.format(question=prompt, answer_a=answer_base, answer_b=answer_test)
        for prompt, answer_basae, answer_test in zip(prompts, formatted_responses_base, formatted_responses_test)
    ]
    gpt_responses = gpt4.batch_prompt(system_message=SYSTEM_PROMPT, messages=formatted_gpt_prompts)
    formatted_gpt_responses = [int(resp[0].split('Final Response:')[1].strip()) for resp in gpt_responses]
    breaktpoin()
  
if __name__ == "__main__":
    fire.Fire(main())