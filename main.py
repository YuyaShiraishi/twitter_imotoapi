import argparse
import os

import logging
from logging.handlers import RotatingFileHandler

from modules import gpt, news, twitter

# ログの定義
logger = logging.getLogger(__name__)
formatter = formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

log_file = './logs/error.log'
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=10)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)

# グローバル変数
error_msg = 'お兄ちゃん、ごめんね。ちょっと今、うまくツイートできなかったみたい。少し待ってね。頑張って情報をお届けするから！(๑•̀ㅂ•́)و✧'
tags = ' #AI妹'


def main():
    # 引数の定義
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prompt', help='入力プロンプト', default='お兄ちゃんが楽しくなる雑談をする')
    args = parser.parse_args()

    # ニュース要約ツイートをする場合はpromptを書き換える
    if args.prompt == '本日のニュース':
        try:
            with open('prompt/news_summary.txt', 'r', encoding='utf-8') as f:
                args.prompt = f.read() + news.fetch()
        except Exception as e:
            logger.exception('News API error occurred.')

    # GPTによるツイート生成
    try:
        tweet_text = gpt.generate_text(args.prompt)
    except Exception as e:
        logger.exception('OpenAI API error occurred.')

        # エラーでGPTが文章を生成できなかったときの代替メッセージを代入
        tweet_text = error_msg

    # タグの挿入
    tweet_text = tweet_text + tags

    # 140字以上になっていたら切り詰める
    if len(tweet_text) >= 140:
        tweet_text = tweet_text[:139]

    # ツイートする
    try:
        twitter.tweet(tweet_text)
    except Exception as e:
        logger.exception('Twitter API error occurred')


if __name__ == "__main__":
    main()
