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
