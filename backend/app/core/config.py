from __future__ import annotations

import os


def _env(key: str, default: str) -> str:
    return os.environ.get(key, default)


class Settings:
    def __init__(self) -> None:
        self.api_key = _env("API_KEY", "dev-api-key")
        self.database_url = _env("DATABASE_URL", "memory://")
        self.redis_url = _env("REDIS_URL", "memory://")
        self.environment = _env("ENVIRONMENT", "development")
        self.forti_verify_ssl = _env("FORTI_VERIFY_SSL", "true").lower() in {"1", "true", "yes"}


settings = Settings()
