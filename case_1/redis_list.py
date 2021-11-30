from typing import Optional, TypedDict

from base import (
    CLIENT_NAME,
    ArticleStruct,
    get_redis_connect,
    create_articles,
    serialize_articles,
    deserialize_articles,
    get_uniq_keys,
    create_article,
    serialize_article,
    invalidate_some_articles,
    is_exist,
    add_articles_to_cache,
)


SPLIT_STR = "-----------------------------\n"


SIMPLE_LIST_CLIENT_NAME = f"simple_list_{CLIENT_NAME}"
LINK_LIST_CLIENT_NAME = f"link_list_{CLIENT_NAME}"


class ListResponse(TypedDict):
    start: Optional[int]
    articles: list[ArticleStruct]


def push_to_redis_list(items: list[str], key: str):
    r = get_redis_connect()
    r.lpush(key, *items)


def simple_create_new_redis_list():
    if is_exist(SIMPLE_LIST_CLIENT_NAME):
        return

    articles = create_articles()
    raw_articles = serialize_articles(articles)
    push_to_redis_list(raw_articles, SIMPLE_LIST_CLIENT_NAME)


def simple_read_articles_from_cache(keys: Optional[list[str]] = None):
    uniq_keys = keys or [f"uniq_key{i}" for i in range(20)]
    r = get_redis_connect()
    raw_articles: list[str] = r.mget(uniq_keys)
    articles: list[ArticleStruct] = deserialize_articles(raw_articles)
    print(articles)


def simple_invalidate_some_articles():
    create_articles(10, suffix="_new")  # Updated some articles
    r = get_redis_connect()
    r.delete(SIMPLE_LIST_CLIENT_NAME)
    simple_create_new_redis_list()


def link_create_new_redis_list():
    if is_exist(LINK_LIST_CLIENT_NAME):
        return

    articles = create_articles()
    add_articles_to_cache(articles)
    articles_keys = get_uniq_keys(articles)
    push_to_redis_list(articles_keys, LINK_LIST_CLIENT_NAME)


def link_add_article_to_redis_list(number: int = 20, suffix: str = ""):
    article = create_article(number, suffix)
    r = get_redis_connect()
    raw_article = serialize_article(article)
    r.set(article["uniq_key"], raw_article)
    push_to_redis_list([article["uniq_key"]], LINK_LIST_CLIENT_NAME)


def link_read_articles_from_list(start: int = 0, end: int = 10) -> ListResponse:
    r = get_redis_connect()
    pipe = r.pipeline()
    pipe.lrange(LINK_LIST_CLIENT_NAME, start, end)
    pipe.llen(LINK_LIST_CLIENT_NAME)
    keys, list_len = pipe.execute()
    raw_articles = r.mget(keys)
    articles: list[ArticleStruct] = deserialize_articles(raw_articles)
    next_id = start + len(articles) + 1
    if next_id >= list_len:
        next_id = None

    return ListResponse(start=next_id, articles=articles)


def check_link_invalidate_some_articles():
    link_read_articles_from_list()
    invalidate_some_articles()
    link_read_articles_from_list()


def check_link_redis_list_pagination(start: int = 5, end: int = 10):
    link_read_articles_from_list(start, end)
    link_add_article_to_redis_list()
    link_read_articles_from_list(start, end)


def test_pagination_redis_list():
    ...
