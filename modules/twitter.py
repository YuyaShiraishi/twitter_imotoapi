import os
import json
from requests_oauthlib import OAuth1Session

import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
formatter = formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# ログファイルのハンドラを作成する
log_file = './logs/tweet.log'
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=10)
file_handler.setFormatter(formatter)

# ロガーにハンドラを設定する
logger.addHandler(file_handler)

# ログの情報レベルを設定する
logger.setLevel(logging.DEBUG)


def tweet(tweet_text):
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    access_token = os.environ.get('ACCESS_TOKEN')
    access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

    oauth = OAuth1Session(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
    )

    payload = {"text": tweet_text}

    try:
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
        )
    except Exception as e:
        raise e

    if response.status_code != 201:
        raise ValueError(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    # Saving the response as JSON
    json_response = response.json()
    logger.debug(json.dumps(json_response, indent=4, sort_keys=True))
