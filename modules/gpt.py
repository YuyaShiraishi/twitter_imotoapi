import openai
import os
import configparser

openai.api_key = os.environ["OPENAI_API_KEY"]

config = configparser.ConfigParser()
config.read('config.ini')

model = config.get('openai', 'model')
temperature = float(config.get('openai', 'temperature'))

def generate_text(prompt):
    with open('prompt_restriction.txt', 'r', encoding='utf-8') as f:
        restriction = f.read()

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "100文字以内で回答する"
            },
            {
                "role": "user",
                "content": restriction
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature,
        max_tokens=200,
    )

    generated_text = response.choices[0].message.content
    return generated_text

