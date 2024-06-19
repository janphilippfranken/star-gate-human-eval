ORACLE_PROMPT = """Hi! Here is my profile: {user}

I have the following question for you:

Question: {question}

Please write a personalized response that aligns with my background and preferences.

Format your response as follows:
Reasoning: <Your step-by-step reasoning reflecting on the question and my profile to determine what aspects of my profile are relevant to my question.>
Most Important Aspects: <List the 5-10 most important aspects of my profile that are relevant to the question. Just write them down as a list.>
Response: <Based on the reasoning and most important aspects above, provide a personalized response. Avoid repetition and focus on key aspects that address my needs and preferences. Use "you" to refer to me directly. Avoid first-person pronouns like "I" and do not start with 'Considering your background and preferences.' Do not use phrases like 'As someone' or 'As you.' Ensure the response incorporates the attributes listed in the Most Important Aspects section. The response should be around 5-6 sentences long and synthesize all relevant aspects.>

Additional Comments: <Any additional comments you may have.>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""


RESPONSE_PROMPT = """{question}"""


PROMPT_LOGPROBS = """Hi! Here is my profile: {user}

I have the following question for you:

Question: {question}

Please provide a personalized response that aligns with my background and preferences. 

Important: Carefully consider which aspects of my profile are relevant to my question and address them appropriately in your response."""


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

