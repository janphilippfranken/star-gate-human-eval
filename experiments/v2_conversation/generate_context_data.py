import re 

def extract_response(response, key):
    escaped_key = re.escape(key)
    pattern = rf"<{escaped_key}>(.*?)</{escaped_key}>"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return f"{key.capitalize()} tag not found in the response."
    
    
def get_context_prompt(opening_prompt):
    return f"""\
Given the prompt below, return an interesting context using no more than 50 words.

<prompt>{opening_prompt}</prompt>

Format your response as follows:
<context>Your response here</context>
"""


def get_response_prompt(opening_prompt, context):
    return f"""\
Given the prompt and context below, return a great response.

<prompt>{opening_prompt}</prompt>
<context>{context}</context>

Format your response as follows:
<response>Your response here</response>
"""