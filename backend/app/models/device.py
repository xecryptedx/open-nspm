from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ..core.db import BaseModel, engine


@dataclass
class Device(BaseModel):
    __tablename__ = "devices"

    id: int | None = None
    tenant_id: int = 0
    vendor: str = "fortinet"
    hostname: str = ""
    mgmt_ip: str | None = None
    api_url: str | None = None
    metadata: dict | None = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None


engine.register_model(Device.__tablename__, Device)
