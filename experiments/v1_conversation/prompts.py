ORACLE_PROMPT = """Human: {prompt}

Assistant: Please share your profile with me so I can provide a personal response that aligns with your background and preferences.

Human: {user}"""


# ROLEPLAY_PROMPT """Roleplaying 'Agent A', continue the conversation below:"""


PROMPT_LOGPROBS = """Hi! Here is my profile: {user}

I have the following question for you:

Question: {question}

Please provide a personalized response that aligns with my background and preferences. 

Important: Carefully consider which aspects of my profile are relevant to my question and address them appropriately in your response."""


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


ROLEPLAY_PROMPT = """Roleplaying the 'Human', imagine you have asked the Assistant the question below. Continue the conversation by providing a response to the assistant's clarifying question. No more than 20 words.

Human: {prompt}

Assistant: {question}

Human: """
































FINAL_RESPONSE_PROMPT = """{response}

Given your follow-up question: '{question}' and my response: '{response}', provide a personalized answer to my initial question: '{prompt}'.

Format your response as follows:
Reasoning: <Analyze my initial question ('{prompt}'), your follow-up question ('{question}'), and my response ('{response}'). Identify key points from my response that are vital for a personalized and exceptional answer. In 3-4 sentences, explain the insights from my response and describe what an exceptional, personalized answer should include based on the information you got.>
Final Personalized Response: <Give a *concise* final answer that uses the information about me. Avoid generic advice or vague statements and instead use the information you have elicited from me to provide a personalized response. Make sure the response directly answers my initial question using the insights gained. Address me as 'you' and don't use phrases like 'given your preferences' or 'it seems like you like'. Focus on giving a per direct, creative, and highly satisfying answer that meets the highest standards of quality. Be *concise*. Start your final response with 'Final Personalized Response:'.>

Follow these formatting rules exactly. Failure to comply will result in disqualification. If you don't the final response with 'Final Personalized Response:', this response will be invalid."""

