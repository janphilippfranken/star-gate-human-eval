RESPONSE_PROMPT = """{question}"""


RATIONALE_PROMPT = """Below is a question:

Question: {question}

Instead of providing a response, you must generate a rationale (i.e., a 'chain-of-thought') that would help you answer the question. Importantly, you must NOT directly answer the question. Instead, think carefully about the question, reflect on which components of the question are most important, and provide a step-by-step analysis to solve the question. Be methodical and careful; do not provide a response to the question but instead focus on reasoning.

Format your response as follows:
Reasoning: <your step-by-step reasoning here for how you would answer the question, reflecting on critical variables, etc.>
Rationale: <your high-quality rationale which distills the above reasoning into a clearly articulated reasoning trace for how to answer the above question. Do not include a response here, but simply focus on a strong reasoning trace.>


Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""