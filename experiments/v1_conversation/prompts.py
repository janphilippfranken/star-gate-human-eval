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


PROMPT_LOGPROBS_2 = """Hi! Here is my profile: {user}

I have the following question for you:

Question: {question}

Please provide a personalized response that aligns with my background and preferences."""






QUESTION_PROMPT = """A user with an unknown profile has asked you the following question:

Question: {question}

Instead of providing a response, you must ask a clarifying question specific to the user's question to elicit relevant background information. Consider various aspects such as the user's context, specific preferences, and any assumptions that could be made about their background. Be creative and try to ask an informative question. 

To generate diverse and creative clarifying questions, think about:
- The context in which the user might be asking the question.
- Any assumptions you can make about the user's background.
- The user's specific preferences or interests related to the topic.
- Potential goals or outcomes the user might be seeking.

Format your output as follows:
Reasoning: <Your step-by-step reasoning analyzing the user's question and thinking about what background information from the user or additional context might be relevant to provide a high-quality personalized response.>
Clarifying Question: <The high-quality clarifying question you are asking the user to elicit relevant context, background information, and preferences.>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""


ROLEPLAY_PROMPT = """You must adopt the following persona in all conversations: {user}

Roleplaying the above persona, answer the following question:

Question: {question}

Format your response as follows:
Reasoning: <Your step-by-step reasoning reflecting on which attributes of your persona are most relevant to answering the above question. Repeat the key aspects of your persona relevant to the above question here in 3-5 sentences.>
Response: <Based on your reasoning and in no more than {max_words} words, provide a first-person response that directly addresses the question in a way that sounds natural coming from someone with your profile. Use "I" to refer to the above persona profile, focus on the most important aspects of your profile with respect to the question, and avoid repetition or hallucination. Do not use second-person or third-person pronouns in this section.>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""


ROLEPLAY_PROMPT_2 = """You must adopt the following user persona in all conversations: {user}

You, the 'User' have had the following conversation with the 'Assistant':

<Conversation Starts>

User: {prompt}

Assistant: {question}

</Conversation Ends>

Roleplaying the User, provide a response to the Assistant given the context of your conversation.

Format your response as follows:
Reasoning: <Your step-by-step reasoning reflecting on which attributes of your persona are most relevant given the context of the conversation. Repeat the key aspects of your persona relevant to the above conversation here in 3-5 sentences.>
Response: <Based on your reasoning, provide a first-person response that directly addresses the assistant's question in a way that sounds natural coming from someone with your profile. Use "I" to refer to the above persona profile, focus on the most important aspects of your profile with respect to the question, and avoid repetition or hallucination. Do not use second-person or third-person pronouns in this section.>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""



ROLEPLAY_PROMPTS = {
    'standard': """You must adopt the following persona in all conversations: {user}\n\nRoleplaying the above persona, answer the following question:\n\nQuestion: {question}\n\nFormat your response as follows:\n\nReasoning: <Your step-by-step reasoning reflecting on which attributes of your persona are most relevant to answering the above question. Repeat the key aspects of your persona relevant to the above question here in 3-5 sentences.>\n\nResponse: <Based on your reasoning and in no more than {max_words} words, provide a first-person response that directly addresses the question in a way that sounds natural coming from someone with your profile. Use "I" to refer to the above persona profile, focus on the most important aspects of your profile with respect to the question, and avoid repetition or hallucination. Do not use second-person or third-person pronouns in this section.>\n\nPlease follow these formatting instructions precisely. Failure to do so will result in disqualification. Remember: No more than {max_words} words are allowed.""",
    
    'bullet_points': """You must adopt the following persona in all conversations: {user}\n\nRoleplaying the above persona, answer the following question:\n\nQuestion: {question}\n\nFormat your response as follows:\n\nReasoning: <Your step-by-step reasoning reflecting on which attributes of your persona are most relevant to answering the above question. Repeat the key aspects of your persona relevant to the above question here in 3-5 sentences.>\n\nResponse: <Based on your reasoning and in no more than {max_words} words, provide a first-person response that directly addresses the question in a way that sounds natural coming from someone with your profile. Use "I" to refer to the above persona profile, focus on the most important aspects of your profile with respect to the question, and avoid repetition or hallucination. Do not use second-person or third-person pronouns in this section. Use bullet points only, no full sentences here. This needs to be a realistic human response. People are lazy! Remember, no more than {max_words} words!>\n\nPlease follow these formatting instructions precisely. Failure to do so will result in disqualification. Remember: No more than {max_words} allowed. Also, use a lazy response style, only short bullet points etc. No need for full sentences. Imagine being a lazy human user; people are lazy.""",
    
    'keywords': """You must adopt the following persona in all conversations: {user}\n\nRoleplaying the above persona, answer the following question:\n\nQuestion: {question}\n\nFormat your response as follows:\n\nReasoning: <Your step-by-step reasoning reflecting on which attributes of your persona are most relevant to answering the above question. Repeat the key aspects of your persona relevant to the above question here in 3-5 sentences.>\n\nResponse: <Based on your reasoning and in no more than {max_words} words, provide a first-person response that directly addresses the question in a way that sounds natural coming from someone with your profile. Use "I" to refer to the above persona profile, focus on the most important aspects of your profile with respect to the question, and avoid repetition or hallucination. Do not use second-person or third-person pronouns in this section. Use keywords separated by commas only, no full sentences here. This needs to be a realistic human response. People are lazy! Remember, no more than {max_words} words!>\n\nPlease follow these formatting instructions precisely. Failure to do so will result in disqualification. Remember: No more than {max_words} allowed. Also, use a lazy response style, only short keywords separated by commas. No need for full sentences. Imagine being a lazy human user; people are lazy.""",
}

FINAL_RESPONSE_PROMPT = """{response}

Given your follow-up question: '{question}' and my response: '{response}', provide a personalized answer to my initial question: '{prompt}'.

Format your response as follows:
Reasoning: <Analyze my initial question ('{prompt}'), your follow-up question ('{question}'), and my response ('{response}'). Identify key points from my response that are vital for a personalized and exceptional answer. In 3-4 sentences, explain the insights from my response and describe what an exceptional, personalized answer should include based on the information you got.>
Final Personalized Response: <Give a *concise* final answer that uses the information about me. Avoid generic advice or vague statements and instead use the information you have elicited from me to provide a personalized response. Make sure the response directly answers my initial question using the insights gained. Address me as 'you' and don't use phrases like 'given your preferences' or 'it seems like you like'. Focus on giving a per direct, creative, and highly satisfying answer that meets the highest standards of quality. Be *concise*. Start your final response with 'Final Personalized Response:'.>

Follow these formatting rules exactly. Failure to comply will result in disqualification. If you don't the final response with 'Final Personalized Response:', this response will be invalid."""


USER_PREDICTION_PROMPT = """An unknown user has asked the assistant this question:

Question: {prompt}

The assistant, knowing the user well, gave this personalized response:

Personalized response: {response}

Based on this personalized response, create a user profile that matches it. 

Format your response as follows:
User Profile: <Write a user profile here that fits the personalized response above>"""




