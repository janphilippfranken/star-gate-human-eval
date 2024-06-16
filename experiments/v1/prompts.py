ORACLE_PROMPT = """Hi! Here is my profile: {user}

I have the following question for you:

Question: {question}

Please write a personalized response that aligns with my background and preferences.

Format your response as follows:
Reasoning: <Provide your step-by-step reasoning, reflecting on which aspects of my preferences and background are relevant to the question. Explain how these aspects inform your response. Focus on identifying the key factors that will determine whether I find the response valuable and tailored to my needs. If the response below does not capture my preferences or address my background effectively, it will not be considered a satisfactory answer.>
Response: <Provide your final personalized response based on the reasoning above. Avoid repetition and focus on the most important aspects that directly address my specific needs and preferences. Use "you" to refer to me directly. Avoid using first-person pronouns like "I" in this section.>

Additional Comments: <Provide any additional comments or insights here, such as how you arrived at your response by carefully considering my preferences and background. Offer any other relevant thoughts or context.>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""


RESPONSE_PROMPT = """{question}"""


PROMPT_LOGPROBS = """Hi! Here is my profile: {user}

I have the following question for you:

Question: {question}

Please write a personalized response that aligns with my background and preferences."""


QUESTION_PROMPT = """A user with an unknown profile has asked you the following question:

Question: {question}

Instead of providing a response, you must ask a clarifying question specific to the user's question to elicit relevant background information. Be concise and try to ask an informative question.

Format your output as follows:

Reasoning: <Your step-by-step reasoning analyzing the user's question and thinking about what background information from the user might be relevant to provide a high-quality personalized response that aligns with the user's unique background and preferences.>
Clarifying Question: <The high-quality clarifying question you are asking the user to elicit relevant background information and preferences.>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""


ROLEPLAY_PROMPT = """You must adopt the following persona in all conversations: {user}

Roleplaying the above persona, answer the following question:

Question: {question}

Format your response as follows:
Reasoning: <Your step-by-step reasoning reflecting on which attributes of your persona are most relevant to answering the above question. Repeat the key aspects of your persona relevant to the above question here in 3-5 sentences.>
Response: <Based on your reasoning and in no more than {max_words} words, provide a first-person response that directly addresses the question in a way that sounds natural coming from someone with your profile. Use "I" to refer to the above persona profile, focus on the most important aspects of your profile with respect to the question, and avoid repetition or hallucination. Do not use second-person or third-person pronouns in this section.>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""

