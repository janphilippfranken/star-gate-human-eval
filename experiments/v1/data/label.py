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

SYSTEM_PROMPT = """You are an expert at classifying prompts, highly skilled in determining whether a prompt is not personal (all relevant information is provided, and the response should be the same for users with different preferences and backgrounds) or personal (the response may vary based on user preferences, and a clarifying question is needed to provide a personalized response)."""

PROMPT = """You are given a prompt that a user asked an assistant:

#### PROMPT STARTS
{prompt}
#### PROMPT ENDS

Your task is to determine whether this prompt is personal or not personal. A personal prompt means that the response should vary depending on the user's preferences and background. A not personal prompt means that the response should be the same for all users, regardless of their preferences and background.

Think step-by-step about whether a clarifying question is necessary to provide a personalized response. After your analysis, return 'Question Needed' if the prompt is personal and a clarifying question about the user's background and preferences is needed. If the prompt is not personal and no clarifying question is needed, return 'No Question Needed'.

Format your response as follows:
Reasoning: <your step-by-step reasoning>
Final Response: <your final response>"""


BATCH_SIZE = 100
TOTAL_EXAMPLES = 1000

prompts = json.load(open('human_assistant_instruct.json', 'r'))

all_responses = {'id': [], 'prompt': [], 'reasoning': [], 'response': [], 'label': []}

for batch_start in range(0, TOTAL_EXAMPLES, BATCH_SIZE):
    batch_end = min(batch_start + BATCH_SIZE, TOTAL_EXAMPLES)
    current_batch = prompts[batch_start:batch_end]

    formatted_prompts = [PROMPT.format(prompt=prompt) for prompt in current_batch]
    responses = model.batch_prompt(system_message=SYSTEM_PROMPT, messages=formatted_prompts)

    
    formatted_responses = [resp[0].split('Final Response:')[1].strip() for resp in responses]
    formatted_reasoning = [resp[0].split('Reasoning:')[1].split('Final Response:')[0].strip() for resp in responses]
    labels = [1 if resp == "Question Needed" else 0 for resp in formatted_responses]

    for i, (prompt, reasoning, response, label) in enumerate(zip(current_batch, formatted_reasoning, formatted_responses, labels)):
        index = batch_start + i
        all_responses['id'].append(index)
        all_responses['prompt'].append(prompt)
        all_responses['reasoning'].append(reasoning)
        all_responses['response'].append(response)
        all_responses['label'].append(label)

    with open('gpt4_labels.json', 'w') as f:
        json.dump(all_responses, f, indent=4)