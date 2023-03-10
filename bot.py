from telethon import TelegramClient, events
import os
import openai
import json
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('API_KEY')
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
botToken = os.getenv('botToken')

client = TelegramClient('Kiyotaka', api_id, api_hash)
client.start(bot_token=botToken)


@client.on(events.NewMessage)
async def event_handler(event):
    user = event.sender_id
    message = event.raw_text

    response = get_response(message, user)

    await event.respond(response)


def get_response(message, user):
    prompt = [

    ]
    if not os.path.exists(f'chats/{user}.json'):
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a ai language model.You know everything. Your name is Kiyotaka Ayanokoji."
                }

            ]

        }
        with open(f'chats/{user}.json', 'w') as f:
            json.dump(data, f, indent=4)

    with open(f'chats/{user}.json', 'r') as f:
        data = json.load(f)['messages']

    # for item in data:
    #   prompt.append(item)
    [prompt.append(item) for item in data]

    prompt.append(
        {
            "role": "user",
            "content": message
        }
    )

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=prompt
    )

    response = completion.choices[0].message.content

    with open(f'chats/{user}.json', 'r') as f:
        data = json.load(f)
    data['messages'].append(
        {
            "role": "user",
            "content": message
        }
    )
    data['messages'].append(
        {
            "role": "assistant",
            "content": response
        }
    )
    with open(f'chats/{user}.json', 'w') as f:
        json.dump(data, f, indent=4)

    return response


client.run_until_disconnected()
