from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .common import ORMBase, Timestamped


@dataclass
class DeviceCreate(ORMBase):
    tenant_id: int
    vendor: str = "fortinet"
    hostname: str = ""
    mgmt_ip: str | None = None
    api_url: str | None = None
    metadata: dict | None = None


@dataclass
class DeviceRead(Timestamped):
    id: int
    tenant_id: int
    vendor: str
    hostname: str
    mgmt_ip: str | None
    api_url: str | None
    metadata: dict | None
    created_at: datetime
    updated_at: datetime | None = None
