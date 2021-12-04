import enum

from typing import Optional, Any

from pydantic import BaseModel, HttpUrl


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
