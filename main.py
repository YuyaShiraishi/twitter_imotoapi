#!/usr/bin/python3

import argparse
import os
from os.path import (
    dirname,
    abspath,
    join,
)
import logging
from logging.handlers import RotatingFileHandler
import random

from modules import gpt, news, twitter

script_dir = dirname(abspath(__file__))

# ログの定義
logger = logging.getLogger(__name__)
formatter = formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_file = join(script_dir, 'logs', 'error.log')

file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=10)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)


def main(args):
    prompt = ''

    # ニュース要約ツイート
    if args.prompt == '今日のニュース':
        # ニュースのトピックについてランダムに選択
        try:
            with open(join(script_dir, 'topics.txt'), 'r', encoding='utf-8') as f:
                topics = f.read().splitlines()
                query = random.choice(topics)
        except Exception as e:
            raise e

        try:
            prompt = news.fetch(query)
            prompt = prompt.replace("\n", "\\n")
        except Exception as e:
            logger.exception('News API error occurred.')
    else:
        prompt = args.prompt

    try:
        # 通常の会話の場合
        if prompt == '':
            tweet_text = gpt.generate_text(prompt)
        else:
            tweet_text = gpt.generate_text_with_fine_tuned(prompt)
    except Exception as e:
        logger.exception('OpenAI API error occurred.')

        # エラーでGPTが文章を生成できなかったときの代替メッセージを代入
        tweet_text = 'お兄ちゃん、ごめんね。ちょっと今、うまくツイートできなかったみたい。少し待ってね。頑張って情報をお届けするから！(๑•̀ㅂ•́)و✧'

    # ツイートする
    try:
        print(query)
        print(prompt)
        print(tweet_text)
        #twitter.tweet(tweet_text)
    except Exception as e:
        logger.exception('Twitter API error occurred')


if __name__ == "__main__":
    # 引数の定義
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prompt', help='入力プロンプト', default='お兄ちゃんが楽しくなる雑談をする')
    args = parser.parse_args()

    main(args)
