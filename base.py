from typing import TypedDict, Optional

from config import env_settings

import redis
import json


CLIENT_NAME = "our_client"
RAW_ARTICLE = str
ARTICLE_UNIQ_KEY = str

UNIQ_KEY_PREFIX = "uniq_key_"


def get_redis_connect():
    return redis.Redis(
        host=env_settings.REDIS_HOST,
        port=env_settings.REDIS_PORT,
        db=env_settings.REDIS_DB,
        password=env_settings.REDIS_PASSWORD,
    )


class ArticleStruct(TypedDict):
    source_url: str
    uniq_key: str
    duration: int
    audio_url: str


def create_article(number: int, suffix: str) -> ArticleStruct:
    article = {
        "source_url": f"https://some_site.com/articles/article_{number}",
        "uniq_key": f"{UNIQ_KEY_PREFIX}{number}",
        "duration": 10 + number,
        "audio_url": f"https://our_media_domain.com/articles/article_{number}{suffix}.mp3",
    }
    return article


def create_articles(count: int = 20, suffix: str = "") -> list[ArticleStruct]:
    articles = []
    for i in range(count):
        article = create_article(i, suffix)
        articles.append(article)

    return articles


def serialize_article(article: ArticleStruct) -> RAW_ARTICLE:
    return json.dumps(article)


def serialize_articles(articles: list[ArticleStruct]) -> list[RAW_ARTICLE]:
    return [serialize_article(article) for article in articles]


def deserialize_article(raw_article: RAW_ARTICLE) -> ArticleStruct:
    return json.loads(raw_article)


def deserialize_articles(raw_articles: list[RAW_ARTICLE]) -> list[ArticleStruct]:
    return [deserialize_article(raw_article) for raw_article in raw_articles]


def get_uniq_keys(articles: list[ArticleStruct]) -> list[ARTICLE_UNIQ_KEY]:
    return [article["uniq_key"] for article in articles]


def add_articles_to_cache(articles: Optional[list[ArticleStruct]] = None):
    articles = articles or create_articles()
    r = get_redis_connect()
    pipe = r.pipeline()
    for article in articles:
        pipe.set(article["uniq_key"], serialize_article(article))

    pipe.execute()


def invalidate_some_articles(suffix: str = "_new"):
    articles = create_articles(10, suffix=suffix)
    r = get_redis_connect()
    pipe = r.pipeline()
    for article in articles:
        pipe.set(article["uniq_key"], serialize_article(article))

    pipe.execute()


def reset_environment(key: str):
    r = get_redis_connect()
    keys = [key]
    for key in r.scan_iter(f"{UNIQ_KEY_PREFIX}*"):
        keys.append(key)

    r.delete(*keys)


def is_exist(key: str) -> bool:
    r = get_redis_connect()
    return bool(r.exists(key))
