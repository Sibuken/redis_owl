def push_to_redis_list(items: list[str], key: str):
    r = get_redis_connect()
    r.lpush(key, *items)


def create_new_redis_list():
    if is_exist(CLIENT_NAME):
        return
    articles = create_articles()
    raw_articles = serialize_articles(articles)
    push_to_redis_list(raw_articles, CLIENT_NAME)


def add_article(number: int = 20, suffix: str = ""):
    article = create_article(number, suffix)
    raw_article = serialize_article(article)
    push_to_redis_list([raw_article], CLIENT_NAME)
