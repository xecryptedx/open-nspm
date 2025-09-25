from datetime import datetime

from pydantic import Field

from .common import ORMBase, Timestamped


class DeviceCreate(ORMBase):
    tenant_id: int
    vendor: str = Field(default="fortinet")
    hostname: str
    mgmt_ip: str | None = None
    api_url: str | None = None
    metadata: dict | None = None


class DeviceRead(Timestamped):
    id: int
    tenant_id: int
    vendor: str
    hostname: str
    mgmt_ip: str | None
    api_url: str | None
    metadata: dict | None
    updated_at: datetime | None
