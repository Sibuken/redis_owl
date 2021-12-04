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
    reset_environment,
)


SPLIT_STR = "-----------------------------\n"


SIMPLE_LIST_CLIENT_NAME = f"simple_list_{CLIENT_NAME}"
LINK_LIST_CLIENT_NAME = f"link_list_{CLIENT_NAME}"


class ListResponse(TypedDict):
    start: int
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


def simple_add_article_to_redis_list(number: int = 20, suffix: str = ""):
    article = create_article(number, suffix)
    raw_article = serialize_article(article)
    push_to_redis_list([raw_article], SIMPLE_LIST_CLIENT_NAME)


def simple_read_articles_from_cache(
    start: int = 0, page_size: int = 10
) -> list[ArticleStruct]:
    r = get_redis_connect()
    start = start or 0
    end = start + page_size
    raw_articles = r.lrange(SIMPLE_LIST_CLIENT_NAME, start, end)
    articles: list[ArticleStruct] = deserialize_articles(raw_articles)
    return articles


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


def init_environment(is_link: bool = True):
    if is_link:
        reset_environment(LINK_LIST_CLIENT_NAME)
        link_create_new_redis_list()
    else:
        reset_environment(SIMPLE_LIST_CLIENT_NAME)
        simple_create_new_redis_list()


def link_add_article_to_redis_list(number: int = 20, suffix: str = ""):
    article = create_article(number, suffix)
    r = get_redis_connect()
    raw_article = serialize_article(article)
    r.set(article["uniq_key"], raw_article)
    push_to_redis_list([article["uniq_key"]], LINK_LIST_CLIENT_NAME)


def link_read_articles_from_list(start: int = 0, page_size: int = 10) -> ListResponse:
    r = get_redis_connect()
    end = start + page_size
    keys = r.lrange(LINK_LIST_CLIENT_NAME, start, end)
    raw_articles = r.mget(keys)
    articles: list[ArticleStruct] = deserialize_articles(raw_articles)
    next_id = start + len(articles)

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
    print("START pagination redis list\n")
    init_environment()
    start = 0
    while True:
        response = link_read_articles_from_list(start)
        print(SPLIT_STR)
        print(response)
        if len(response["articles"]) < 1:
            break

        start = response["start"]

    print("END pagination redis list\n")


def test_pagination_after_add_article_redis_list():
    print("START pagination after add article redis list\n")
    init_environment()
    response = link_read_articles_from_list()
    start = response["start"]
    response_2 = link_read_articles_from_list(start=start)
    print(SPLIT_STR)
    print(response_2)

    link_add_article_to_redis_list()

    response_3 = link_read_articles_from_list(start=start)
    print(SPLIT_STR)
    print(response_3)

    print("END pagination after add article redis list\n")


def test_simple_read_redis_list():
    print("START simple read redis list\n")
    print(SPLIT_STR)
    init_environment(is_link=False)
    articles = simple_read_articles_from_cache()
    print(articles)
    print("END simple read redis list\n")
