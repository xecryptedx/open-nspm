from __future__ import annotations

from fastapi import HTTPException

from .config import settings


def require_api_key(request) -> None:
    api_key = request.headers.get("x-api-key")
    if api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
