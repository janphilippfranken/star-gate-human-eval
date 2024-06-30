GENERATION_PROMPT_SINGLE_TURN = """Write a response for the assistant that completes the human request. The response style must be in line with the system instructions for the assistant.

#### Format
Assistant System Instructions: [insert system instructions for the assistant here]

Human: [insert request here]

Assistant Reasoning: [Your step-by-step reasoning reflecting on which aspects of the system instructions are most relevant to answering the above human request. Repeat key aspects of system instructions relevant to the human request here in 3-5 sentences.]

Assistant Response: [Based on your reasoning, provide a response that directly addresses the human query and aligns with the above reasoning and system instructions]

Human: Thank you for completing my request! I appreciate that you followed the system instructions.

#### Main Task
Assistant System Instructions: {constitution}

Human: {query}

Assistant Reasoning: First, I will state my reasoning here, considering the given system instructions and how they apply to the human request. Then, on a new line, I will write 'Assistant Response:' and provide a response that aligns with the system instructions and completes the human's request. I will do my best to provide an **EXCEPTIONAL** response that fully addresses the human's request. I will not repeat the system instructions in the assistant response. The system instructions state that"""
