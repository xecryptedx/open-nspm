from collections.abc import Generator
from typing import Any

import httpx


class FortinetClient:
    """Minimal FortiGate REST client with pagination helpers."""

    def __init__(
        self,
        base_url: str,
        token: str,
        verify_ssl: bool = True,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self._client = httpx.Client(verify=verify_ssl, timeout=timeout)

    def _headers(self) -> dict[str, str]:
        return {"X-Auth-Token": self.token}

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        response = self._client.request(method, url, headers=self._headers(), params=params)
        response.raise_for_status()
        return response.json()

    def _paginate(self, path: str, params: dict[str, Any] | None = None) -> Generator[Any, None, None]:
        params = params.copy() if params else {}
        offset = params.get("offset", 0)
        limit = params.get("limit", 100)
        while True:
            params.update({"offset": offset, "limit": limit})
            payload = self._request("GET", path, params=params)
            if isinstance(payload, dict) and "results" in payload:
                results = payload.get("results", [])
                for item in results:
                    yield item
                if len(results) < limit:
                    break
            else:
                data = payload.get("data", []) if isinstance(payload, dict) else []
                for item in data:
                    yield item
                if len(data) < limit:
                    break
            offset += limit

    def list_policies(self) -> list[dict[str, Any]]:
        return list(self._paginate("/api/v2/cmdb/firewall/policy"))

    def list_addresses(self) -> list[dict[str, Any]]:
        return list(self._paginate("/api/v2/cmdb/firewall/address"))

    def list_services(self) -> list[dict[str, Any]]:
        return list(self._paginate("/api/v2/cmdb/firewall/service/custom"))

    def list_interfaces(self) -> list[dict[str, Any]]:
        return list(self._paginate("/api/v2/cmdb/system/interface"))

    def download_config_backup(self) -> bytes:
        payload = self._request("GET", "/api/v2/monitor/system/config/backup")
        if isinstance(payload, dict) and "results" in payload:
            return payload["results"].encode()
        if isinstance(payload, (bytes, bytearray)):
            return bytes(payload)
        if isinstance(payload, str):
            return payload.encode()
        return b""

    def close(self) -> None:
        self._client.close()
