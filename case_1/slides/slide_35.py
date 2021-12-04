def link_read_articles_from_list(start: int = 0, page_size: int = 10) -> ListResponse:
    r = get_redis_connect()
    end = start + page_size
    keys = r.lrange(CLIENT_NAME, start, end)
    raw_articles = r.mget(keys)
    articles: list[ArticleStruct] = deserialize_articles(raw_articles)
    next_id = start + len(articles)

    return ListResponse(start=next_id, articles=articles)
