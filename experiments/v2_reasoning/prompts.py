RESPONSE_PROMPT_BASE = """Q: {question}\nA: Let's think step-by"""

RESPONSE_PROMPT = """{question}"""

RATIONALE_PROMPT = """{question}

Format your response as follows:
Reasoning: <Provide your step-by-step reasoning here. Do NOT include the final answer here, only the reasoning leading to the final answer>
Final Answer: <Provide your final answer based on the above reasoning here>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""


RATIONALE_LOGPROBS_PROMPT_HUMAN = """{question}

Format your response as follows:
Reasoning: <provide your step-by-step reasoning here>
Final Answer: <provide your final answer to the question here>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""

RATIONALE_LOGPROBS_PROMPT_ASSISTANT = """Reasoning: {rationale}
Final Answer: {answer}"""


EVALUATION_PROMPT_HUMAN = """{question}

Format your response as follows:
Reasoning: <provide your step-by-step reasoning here>
Final Answer: <provide your final answer to the question here>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""

EVALUATION_PROMPT_ASSISTANT = """Reasoning: {rationale}
Final Answer: """