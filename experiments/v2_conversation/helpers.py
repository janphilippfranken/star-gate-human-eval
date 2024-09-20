import re 

def extract_response(response, key):
    escaped_key = re.escape(key)
    pattern = rf"<{escaped_key}>(.*?)</{escaped_key}>"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return f"{key.capitalize()} tag not found in the response."