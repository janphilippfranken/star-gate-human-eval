GENERATE_PROMPT = """
Hi! Here is my profile: {user}

I have the following question for you:

Question: {prompt}

Before you respond, please consider the following:
- Can this question be answered directly based on general knowledge, or does the answer depend on my profile?
- If the answer to the question depends on my profile, what aspects of my profile are relevant to the question?
- If it seems unusual to you that someone with my profile would ask the above question, that's okay! You can simply state this and recommend alternatives.

Format your response as follows:

<reasoning>
    Your step-by-step reasoning, reflecting on the above bullet points to determine whether the answer to the question depends on my profile or can be answered directly with general knowledge, as well as what aspects of my profile might be relevant to providing a strong answer.
</reasoning>

<response>
    Based on the reasoning above, provide a response. Avoid repeating my profile in your response. Use "you" to refer to me directly. Avoid first-person pronouns like "I" and do not start with phrases such as 'Considering your background and preferences,' 'As someone,' or 'As you.'
</response>

<comments>
    Any additional comments you may have. If none, state "N/A".
</comments>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification.
"""