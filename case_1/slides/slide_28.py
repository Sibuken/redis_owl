def simple_read_articles_from_cache(
    start: int = 0, page_size: int = 10
) -> list[ArticleStruct]:
    r = get_redis_connect()
    end = start + page_size
    raw_articles = r.lrange(CLIENT_NAME, start, end)
    articles: list[ArticleStruct] = deserialize_articles(raw_articles)
    return articles
