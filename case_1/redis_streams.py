from typing import Optional, TypedDict

from base import (
    ArticleStruct,
    CLIENT_NAME,
    get_redis_connect,
    create_articles,
    get_uniq_keys,
    create_article,
    serialize_article,
    is_exist,
    add_articles_to_cache,
    deserialize_articles,
    invalidate_some_articles,
    reset_environment,
)


SPLIT_STR = "-----------------------------\n"

DEFAULT_MAX_LEN = 100
STREAM_CLIENT_NAME = f"simple_list_{CLIENT_NAME}"


class StreamResponse(TypedDict):
    start_id: str
    articles: list[ArticleStruct]


def push_to_redis_stream(items: list[str], max_len: int = DEFAULT_MAX_LEN):
    r = get_redis_connect()
    pipe = r.pipeline()
    for value in items:
        pipe.xadd(STREAM_CLIENT_NAME, {"key": value}, maxlen=max_len)

    pipe.execute()


def create_new_redis_stream():
    if is_exist(STREAM_CLIENT_NAME):
        return

    articles = create_articles()
    add_articles_to_cache(articles)
    articles_keys = get_uniq_keys(articles)
    push_to_redis_stream(articles_keys)


def add_article_to_redis_stream(number: int = 20, suffix: str = ""):
    article = create_article(number, suffix)
    r = get_redis_connect()
    raw_article = serialize_article(article)
    r.set(article["uniq_key"], raw_article)
    push_to_redis_stream([article["uniq_key"]])


def read_data_from_redis_stream(
    start_id: Optional[str] = None, count: int = 5
) -> Optional[StreamResponse]:
    start = start_id or "-"
    end = "+"
    r = get_redis_connect()
    data = r.xrange(STREAM_CLIENT_NAME, f"{start}", end, count)
    if len(data) < 1:
        return

    keys = [item[1][b"key"] for item in data]
    raw_articles = r.mget(keys)
    articles = deserialize_articles(raw_articles)
    next_id = data[-1][0].decode()
    response = StreamResponse(start_id=f"({next_id}", articles=articles)
    return response


def read_ordered_data_from_stream(
    start_id: Optional[str] = None, count: int = 5
) -> Optional[StreamResponse]:
    start = start_id or "+"
    end = "-"
    r = get_redis_connect()
    data = r.xrevrange(STREAM_CLIENT_NAME, start, end, count)
    if len(data) < 1:
        return

    keys = [item[1][b"key"] for item in data]
    raw_articles = r.mget(keys)
    articles = deserialize_articles(raw_articles)
    next_id = data[-1][0].decode()
    response = StreamResponse(start_id=f"({next_id}", articles=articles)
    return response


def init_environment():
    reset_environment(STREAM_CLIENT_NAME)
    create_new_redis_stream()


def test_invalidation_redis_stream():
    print("START invalidation redis stream\n")
    init_environment()
    response = read_data_from_redis_stream()
    print(response)
    print(SPLIT_STR)
    invalidate_some_articles()
    response = read_data_from_redis_stream()
    print(response)
    print("END invalidation redis stream\n")


def test_push_new_article_redis_stream():
    print("START push new article to redis stream\n")
    init_environment()
    response = read_ordered_data_from_stream()
    print(response)
    print(SPLIT_STR)
    add_article_to_redis_stream()
    response = read_ordered_data_from_stream()
    print(response)
    print("END push new article to redis stream\n")


def test_pagination_redis_stream():
    print("START pagination redis stream\n")
    init_environment()
    start_id = None
    while True:
        response = read_ordered_data_from_stream(start_id)
        print(SPLIT_STR)
        print(response)
        if response is None:
            break

        start_id = response["start_id"]

    print("END pagination redis stream\n")


def test_pagination_after_add_article_redis_stream():
    print("START pagination after add article redis stream\n")
    init_environment()
    response = read_ordered_data_from_stream()
    start_id = response["start_id"]
    response_2 = read_ordered_data_from_stream(start_id=start_id)
    print(SPLIT_STR)
    print(response_2)

    add_article_to_redis_stream()

    response_3 = read_ordered_data_from_stream(start_id=start_id)
    print(SPLIT_STR)
    print(response_3)

    print("END pagination after add article redis stream\n")
