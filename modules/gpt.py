import openai
import os
import configparser
from os.path import (
    dirname,
    abspath,
    join,
)

openai.api_key = os.environ["OPENAI_API_KEY"]
fine_tuned_model = openai.FineTuningJob.retrieve(os.environ["OPENAI_API_IMOTOAPI_JOBID"]).fine_tuned_model

script_dir = dirname(abspath(__file__))

config = configparser.ConfigParser()
config.read(join(script_dir, '..', 'config.ini'))

model = config.get('openai', 'model')
temperature = float(config.get('openai', 'temperature'))

def generate_text(prompt):
    try:
        with open(join(script_dir, '..', 'prompt', 'restriction.txt'), 'r', encoding='utf-8') as f:
            restriction = f.read()
    except Exception as e:
        raise e

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
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
    except Exception as e:
        raise e

    generated_text = response.choices[0].message.content
    return generated_text

def generate_text_with_fine_tuned(prompt):
    try:
        response = openai.ChatCompletion.create(
            model=fine_tuned_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
    except Exception as e:
        raise e

    generated_text = response.choices[0].message.content
    return generated_text

