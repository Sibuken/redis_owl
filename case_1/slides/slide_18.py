def create_article(number: int, suffix: str) -> ArticleStruct:
    article = {
        "source_url": f"https://some_site.com/articles/article_{number}",
        "uniq_key": f"{UNIQ_KEY_PREFIX}{number}",
        "duration": 10 + number,
        "audio_url": f"https://our_media_domain.com/articles/article_{number}{suffix}.mp3",
    }
    return article
