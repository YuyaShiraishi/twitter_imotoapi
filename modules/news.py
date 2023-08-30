from newsapi import NewsApiClient
from os.path import (
    dirname,
    abspath,
    join,
)
import os
import configparser
import random

api_key = os.environ["NEWS_API_KEY"]
script_dir = dirname(abspath(__file__))

config = configparser.ConfigParser()
config.read(join(script_dir, '..', 'config.ini'))

language  = config.get('newsapi', 'language')
page_size = int(config.get('newsapi', 'page_size'))
sort_by   = config.get('newsapi', 'sort_by')

def fetch(query='ニュース'):
    newsapi = NewsApiClient(api_key=api_key)

    try:
        articles = newsapi.get_everything(q=query,
                                      language=language,
                                      sort_by=sort_by,
                                      page_size=page_size)
    except Exception as e:
        raise e

    news_text = ''
    article = random.choice(articles['articles'])
    news_text += f"{article['title']} - {article['source']['name']}\n"
    news_text += f"URL: {article['url']}\n"
    news_text += f"abstract: {article['description']}\n\n"

    return news_text
