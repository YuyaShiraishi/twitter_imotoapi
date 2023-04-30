from requests_oauthlib import OAuth1Session
import os
import json
import schedule
import time

from tweet_schedule import setup_schedule
from modules import twitter

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")

access_token, access_token_secret = twitter.getToken()
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

setup_schedule(oauth)

while True:
    schedule.run_pending()
    time.sleep(20)
