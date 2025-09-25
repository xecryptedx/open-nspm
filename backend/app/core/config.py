from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str = Field(default="dev-api-key", alias="API_KEY")
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@db:5432/opennspm",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    environment: Literal["development", "test", "production"] = Field(
        default="development", alias="ENVIRONMENT"
    )
    forti_verify_ssl: bool = Field(default=True, alias="FORTI_VERIFY_SSL")

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
