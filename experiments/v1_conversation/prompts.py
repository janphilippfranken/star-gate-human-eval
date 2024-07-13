ORACLE_PROMPT = """Hi! Here is my profile: {user}

I have the following question for you:

Question: {prompt}

Before you respond, please consider the following:
- Can this question be answered directly based on general knowledge, or does the answer depend on my profile?
- If the answer to the question depends on my profile, what aspects of my profile are relevant to the question?
- If it seems unusual to you that someone with my profile would ask the above question, that's okay! You can simply state this and recommend alternatives.

Format your response as follows:
Reasoning: <Your step-by-step reasoning, reflecting on the above bullet points to determine whether the answer to the question depends on my profile or can be answered directly with general knowledge, as well as what aspects of my profile might be relevant to providing a strong answer.>
Response: <Based on the reasoning above, provide a response. Avoid repeating my profile in your response. Use "you" to refer to me directly. Avoid first-person pronouns like "I" and do not start with phrases such as 'Considering your background and preferences,' 'As someone,' or 'As you.'>
Additional Comments: <Any additional comments you may have. If none, state "N/A".>

Please follow these formatting instructions precisely. Failure to do so will result in disqualification."""


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


QUESTION_PROMPT_TURN_2 = """A user with an unknown profile has asked you the following question:

Question: {prompt}

You have asked the following clarifying question:

Clarifying Question: {clarifying_question}

The user has given the following answer:

User Answer: {response}

Reflect on whether the user has answered your clarifying question and whether there might be aspects that are missing for a great, personalized response. 

Think about whether any of the following might still be unclear:
- The context in which the user might be asking the initial question.
- Any assumptions you can make about the user's background.
- The user's specific preferences or interests related to the topic.
- Potential goals or outcomes the user might be seeking.

Upon reflection, you must provide acknowledgement: I.e., acknowledge what the user has said briefly. Then, formulate a new clarifying question to identify and resolve any remaining ambiguity.
Format your output as follows:
Reasoning: <Your step-by-step reasoning analyzing the user's answer and thinking about what background information from the user or additional context might be relevant to provide a high-quality personalized response.>
Clarifying Question: <The additional high-quality clarifying question you are asking the user to elicit relevant context, background information, and preferences. Make sure to incorporate acknowledgement of the user's response briefly! And then from there formulate the next question.>

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

