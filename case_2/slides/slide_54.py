def cache_speakers():
    redis_connect = get_redis_connect()
    all_speakers = creates_speakers()
    if all_speakers is None:
        return False

    grouped_speakers = group_speakers(all_speakers)

    raw_speakers = {}
    for book_language, speakers in grouped_speakers.items():
        key = create_language_group_cache_key(book_language)
        raw_speakers_language = json.dumps([speaker.dict() for speaker in speakers])
        raw_speakers[key] = raw_speakers_language

    redis_connect.hmset(SPEAKERS_CACHE_KEY, raw_speakers)
