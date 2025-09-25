from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from .config import settings


API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_api_key(api_key: str | None = Security(api_key_header)) -> str:
    if api_key and api_key == settings.api_key:
        return api_key
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")


def api_key_dependency(api_key: str = Depends(get_api_key)) -> str:
    return api_key
