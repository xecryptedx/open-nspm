from __future__ import annotations

from collections.abc import Generator
from typing import Any


class FortinetClient:
    """Simple stub client used for offline processing and tests."""

    def __init__(self, base_url: str, token: str, verify_ssl: bool = True, timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.verify_ssl = verify_ssl
        self.timeout = timeout

    def _paginate(self, items: list[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        for item in items:
            yield item

    def list_policies(self) -> list[dict[str, Any]]:
        return []

    def list_addresses(self) -> list[dict[str, Any]]:
        return []

    def list_services(self) -> list[dict[str, Any]]:
        return []

    def list_interfaces(self) -> list[dict[str, Any]]:
        return []

    def download_config_backup(self) -> bytes:
        return b""

    def close(self) -> None:
        return None
