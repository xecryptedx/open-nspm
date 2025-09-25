from __future__ import annotations

from typing import Any

from ..services.fortinet_client import FortinetClient
from ..services.normalizer import normalize_fortigate_payload


class FortiGateAPIImporter:
    def __init__(self, client: FortinetClient) -> None:
        self.client = client

    def collect(self) -> dict[str, Any]:
        payload = {
            "addresses": self.client.list_addresses(),
            "services": self.client.list_services(),
            "policies": self.client.list_policies(),
            "interfaces": self.client.list_interfaces(),
        }
        return normalize_fortigate_payload(payload)
