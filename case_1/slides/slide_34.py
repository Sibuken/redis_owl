def create_new_redis_list():
    if is_exist(CLIENT_NAME):
        return
    articles = create_articles()
    add_articles_to_cache(articles)
    articles_keys = get_uniq_keys(articles)
    push_to_redis_list(articles_keys, CLIENT_NAME)


def add_article(number: int = 20, suffix: str = ""):
    article = create_article(number, suffix)
    r = get_redis_connect()
    raw_article = serialize_article(article)
    r.set(article["uniq_key"], raw_article)
    push_to_redis_list([article["uniq_key"]], CLIENT_NAME)
