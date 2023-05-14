import openai

API_KEY = "#Your API key"
openai.api_key = API_KEY

model_id = 'gpt-3.5-turbo'


def main(prompt):
    def chatConversation(conversation):
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=conversation
        )
        conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
        return conversation

    conversation = [{'role': 'system', 'content': 'How can I help you?'}, {'role': 'user', 'content': prompt}]

    conversation = chatConversation(conversation)
    return '{0}\n'.format(conversation[-1]['content'].strip())
