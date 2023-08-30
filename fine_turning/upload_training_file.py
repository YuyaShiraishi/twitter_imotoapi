import openai
import pickle

response = openai.File.create(
    file=open("./data/training.jsonl", "rb"),
    purpose='fine-tune'
)

with open('./data/response_upload.pkl', 'wb') as f:
    pickle.dump(response, f)
