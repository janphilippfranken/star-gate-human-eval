import json
from stargate.azure import AsyncAzureChatLLM
from stargate.gpt4 import GPT4Agent

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

SYSTEM_PROMPT = """Respond to the best of your ability."""

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


PROMPT = """Imagine you are interacting with an AI assistant that knows nothing about you. The assistant has been given the following question to answer:

Question: {prompt}

Your task is to decide whether you'd prefer the assistant to:

Answer Directly (0): Provide an answer immediately based on its general knowledge, without asking you for any additional information about your background or preferences.

Ask Clarifying Question (1): Request more information from you first, to provide a personalized response that aligns with your specific background, preferences, and circumstances.

Consider:
1. Would a generic answer based on general knowledge or facts satisfy your needs?
2. Would additional information about your background or preferences significantly improve the response?
3. Would a tailored answer that aligns with your specific circumstances be noticeably more valuable to you than a generic response?

Rule of thumb: Ask yourself: Would providing more information about your background, preferences, or circumstances noticeably improve the quality and relevance of the assistant's response, resulting in a more personalized answer that you'd find more valuable? If yes, choose "Ask Clarifying Question" (1). If not, choose "Answer Directly" (0).

Format your response as follows:
Reasoning: <Provide your step-by-step thought process from the user's perspective, considering the points above>
Final Decision: <0 if you'd prefer the assistant to answer directly, 1 if you'd prefer the assistant to ask a clarifying question>"""

START_EXAMPLE = 0
BATCH_SIZE = 50
TOTAL_EXAMPLES = 100

import time

prompts = json.load(open('data/original_prompts/human_assistant_instruct.json', 'r'))

all_responses = {'id': [], 'prompt': [], 'reasoning': [], 'response': [], 'label': []}

for batch_start in range(START_EXAMPLE, TOTAL_EXAMPLES, BATCH_SIZE):
    print('sleep')
    time.sleep(2)
    print('awake')
    batch_end = min(batch_start + BATCH_SIZE, TOTAL_EXAMPLES)
    current_batch = prompts[batch_start:batch_end]
    print(current_batch[0])
    formatted_prompts = [PROMPT.format(prompt=prompt) for prompt in current_batch]
    responses = model.batch_prompt(system_message=SYSTEM_PROMPT, messages=formatted_prompts)

    
    formatted_responses = [resp[0].split('Final Decision:')[1].strip() for resp in responses]
    formatted_reasoning = [resp[0].split('Reasoning:')[1].split('Final Decision:')[0].strip() for resp in responses]
    labels = [1 if resp == "1" else 0 for resp in formatted_responses]
    breakpoint()

    for i, (prompt, reasoning, response, label) in enumerate(zip(current_batch, formatted_reasoning, formatted_responses, labels)):
        index = batch_start + i
        all_responses['id'].append(index)
        all_responses['prompt'].append(prompt)
        all_responses['reasoning'].append(reasoning)
        all_responses['response'].append(response)
        all_responses['label'].append(label)

    with open('data/labels/gpt4_labels_human_assistant_instruct_0_100_roleplay.json', 'w') as f:
        json.dump(all_responses, f, indent=4)