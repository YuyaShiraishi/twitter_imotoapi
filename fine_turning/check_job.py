import openai
import pickle

with open('./data/response_job.pkl', 'rb') as f:
    loaded_data = pickle.load(f)

print(loaded_data)
