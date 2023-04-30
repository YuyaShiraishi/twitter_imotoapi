import schedule
import functools
from modules import twitter

def setup_schedule(oauth):
    # スケジュール
    tweet_with_oauth = functools.partial(twitter.tweet, oauth)

    schedule.every().day.at("08:00").do(tweet_with_oauth)
    schedule.every().day.at("18:00").do(tweet_with_oauth)
    schedule.every().day.at("22:00").do(tweet_with_oauth)
