from newsapi import NewsApiClient
import random
import os
import configparser

api_key = os.environ["NEWS_API_KEY"]

config = configparser.ConfigParser()
config.read('config.ini')

language = config.get('newsapi', 'language')
sort_by = config.get('newsapi', 'sort_by')
page_size = int(config.get('newsapi', 'page_size'))

def fetch(filename='topics.txt'):
    newsapi = NewsApiClient(api_key=api_key)

    with open(filename, 'r', encoding='utf-8') as f:
        topics = f.read().splitlines()

    query = random.choice(topics)

    articles = newsapi.get_everything(q=query,
                                      language=language,
                                      sort_by=sort_by,
                                      page_size=page_size)

    news_text = ""
    for i, article in enumerate(articles['articles']):
        news_text += f"{i + 1}. {article['title']} - {article['source']['name']}\n"
        news_text += f"URL: {article['url']}\n"
        news_text += f"abstract: {article['description']}\n\n"

    return news_text
