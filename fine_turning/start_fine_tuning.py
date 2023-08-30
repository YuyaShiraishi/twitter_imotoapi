import openai
import pickle

with open('./data/response_upload.pkl', 'rb') as f:
    loaded_data = pickle.load(f)

response_job = openai.FineTuningJob.create(training_file=loaded_data.id, model="gpt-3.5-turbo")

with open('./data/response_job.pkl', 'wb') as f:
    pickle.dump(response_job, f)
