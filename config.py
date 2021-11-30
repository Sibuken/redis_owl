from typing import Optional

from pydantic import BaseConfig


class Settings(BaseConfig):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 63790
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None


env_settings = Settings()
