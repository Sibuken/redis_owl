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
