def get_cached_speakers_language_group(book_languages: list[str]) -> list[Speaker]:
    redis_connect = get_redis_connect()
    keys = [book_language for book_language in book_languages]
    data = redis_connect.hmget(SPEAKERS_CACHE_KEY, keys)
    speakers = []
    for raw_speakers in data:
        if raw_speakers:
            speakers += parse_obj_as(list[Speaker], json.loads(raw_speakers))

    return speakers


def get_cached_speakers() -> list[Speaker]:
    redis_connect = get_redis_connect()
    raw_speakers = redis_connect.hvals(SPEAKERS_CACHE_KEY)

    speakers = []
    for raw_speakers in raw_speakers:
        speakers += parse_obj_as(list[Speaker], json.loads(raw_speakers))

    return speakers
