import enum
import collections
import json

from typing import Optional, Any

from pydantic import BaseModel, HttpUrl, parse_obj_as
from base import (
    get_redis_connect,
    is_exist,
    reset_environment,
)


class BookLanguageEnum(str, enum.Enum):
    RUSSIAN = "russian"
    ENGLISH = "english"
    POLISH = "polish"
    CZECH = "czech"
    DANISH = "danish"


class Speaker(BaseModel):
    id: int
    slug: str
    active: bool
    name: dict[str, str]
    sample: Optional[HttpUrl] = None
    is_recommended: bool
    extra_params: Optional[dict[str, Any]]
    book_language: BookLanguageEnum
    duration_ratio: Optional[float] = None
    rating: Optional[float] = None
    provider_information: Optional[dict[str, Optional[str]]] = None


def creates_speakers() -> list[Speaker]:
    speakers = []
    counter_id = 1
    for language in BookLanguageEnum:
        for _ in range(3):
            slug = f"{language.value}_speaker_{counter_id}"
            speaker = Speaker(
                id=counter_id,
                slug=slug,
                active=True,
                name={"eng": slug},
                is_recommended=True,
                extra_params={},
                book_language=language.value,
            )
            speakers.append(speaker)
            counter_id += 1

    return speakers


def group_speakers(speakers: list[Speaker]) -> dict[str, list[Speaker]]:
    grouped_speakers = collections.defaultdict(list)
    for speaker in speakers:
        book_language = speaker.book_language
        grouped_speakers[book_language].append(speaker)

    return grouped_speakers


CACHE_TTL = 600
SPEAKERS_CACHE_KEY = "owl_speakers"


def create_language_group_cache_key(book_language: str) -> str:
    return f"book_language_{book_language}"


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


def get_cached_speakers_language_group(book_languages: list[str]) -> list[Speaker]:
    redis_connect = get_redis_connect()
    keys = [
        create_language_group_cache_key(book_language)
        for book_language in book_languages
    ]
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


def init_environment():
    reset_environment(SPEAKERS_CACHE_KEY)
    cache_speakers()


def test_get_all_speakers_from_cache():
    init_environment()
    speakers = get_cached_speakers()
    print(speakers)


def test_get_speakers_by_language():
    init_environment()
    speakers = get_cached_speakers_language_group(["russian", "english"])
    print(speakers)
