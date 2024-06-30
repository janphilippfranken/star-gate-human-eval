import re

def format_response(response):
    formatted_response = ""
    try:
        formatted_response = response.split("Q:")[0].strip().lower()
    except:
        print("invalid, continue")
    return formatted_response

def extract_answer(answer):
    """Extract gsm answer."""
    if '=' in answer:
        answer = answer.split('=')[-1].strip()
    answer = answer.replace(",", "")
    try: 
        answer = re.findall(r'\d+\.\d+|\d+', answer.strip())[-1]
        answer = round(float(answer), 1)
    except:
        answer = "[invalid]"
    
    return answer


def evaluate_model_response(model_answer, gt_answer):
    """Check if model response is same as ground truth."""
    try:
        result = round(float(model_answer), 1) == round(float(gt_answer), 1)
        return result
    except:
        return False