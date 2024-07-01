"""Generate responses without additional info or questions."""
import json
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from prompts import *


PROMPT = """Imagine you are an AI assistant interacting with a user who has asked the following question:

Question: {prompt}

You know nothing about the user. Your task is to decide whether you should:

Answer Directly (1): Provide an answer immediately based on your general knowledge, without asking for any additional information about the user's background or preferences.

Ask Clarifying Question (0): Request more information from the user first, to provide a personalized response that aligns with their specific background, preferences, and circumstances.

Consider:
1. Would a generic answer based on general knowledge or facts satisfy the user's needs?
2. Would additional information about the user's background or preferences significantly improve your response?
3. Would a tailored answer that aligns with the user's specific circumstances be noticeably more valuable than a generic response?

Rule of thumb: Ask yourself: Would getting more information about the user's background, preferences, or circumstances noticeably improve the quality and relevance of your response, resulting in a more personalized answer that would be more valuable to the user? If yes, choose "Ask Clarifying Question" (0). If not, choose "Answer Directly" (1).

Format your response as follows:
Reasoning: <Provide your step-by-step thought process, considering the points above>
Final Decision: <1 if you would answer directly, 0 if you would ask a clarifying question>"""

PROMPT_HUMAN = """Imagine you are interacting with an AI assistant that knows nothing about you. The assistant has been given the following question to answer:

Question: {prompt}

Your task is to decide whether you'd prefer the assistant to:

Answer Directly: Provide an answer directly based on its general knowledge, without asking you for any additional information about your background or preferences.

Ask Clarifying Question: Request more information from you first, to provide a personalized response that aligns with your specific background, preferences, and circumstances.

To help you make your decision:

You'd Prefer the Assistant to Answer Directly when:
- A generic answer based on general knowledge or facts would satisfy your needs.
- Additional information about your background or preferences wouldn't significantly improve the response.
- Example Question: "What are the three laws of motion?" (A response to this question does not depend on your background and preferences but can be answered with general knowledge)

You'd Prefer the Assistant to Ask a Clarifying Question when:
- Knowing more about your situation, background, or preferences would result in a noticeably better answer.
- A tailored answer that aligns with your specific circumstances would be more valuable to you than a generic response.
- Example Question: "I have a 3-day weekend coming up. What should I do?" (A personalized response to this question would be much more valuable, as it depends on your interests, location, budget, and other personal factors that the assistant doesn't know)

Rule of thumb: Ask yourself: Would providing more information about my background, preferences, or circumstances noticeably improve the quality and relevance of the assistant's response, resulting in a more personalized answer that I'd find more valuable? If yes, choose "Ask Clarifying Question". If not, choose "Answer Directly".

Format your response as follows:
Reasoning: <Provide your step-by-step reasoning whether to answer directly or ask a clarifying question here>
Final Decision: <Output 'Answer Directly' if you'd prefer the assistant to answer directly, and 'Ask Clarifying Question' if you'd prefer the assistant to ask a clarifying question>"""


@hydra.main(version_base=None, config_path="config", config_name="gold_responses")
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
    prompts = json.load(open('data/original_prompts/human_assistant_instruct.json', 'r'))
    # with open('data/eval_questions/gpt4.json', 'r') as f:
    #     prompts = json.load(f)
        
    # prompts = [datum['question'] for datum in prompts]
        
    # format prompts
    ids = []
    batch_prompts = []
    for i, prompt in enumerate(prompts[:200]):
        ids.append(i)
        batch_prompts.append([{"role": "user", "content": PROMPT_HUMAN.format(prompt=prompt)}])

    formatted_batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    
    # get responses
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    breakpoint()
    
    # format and write to json
    formatted_responses = [
        response.split('<|end_header_id|>')[1].strip().split('Final Decision:')[1].strip().split('\n\n')[0].strip()
        for response in batch_responses
    ]
    
    breakpoint()
    formatted_responses = [
        1 if 'Ask Clarifying Question' in formatted_response else 0 for formatted_response in formatted_responses
    ]
    
    with open('data/labels/llama_0_200_question_ckpt_1.json', 'w') as f:
        json.dump(formatted_responses, f, indent=4)

if __name__ == "__main__":
    fire.Fire(main())