from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ..core.db import BaseModel, engine


@dataclass
class Tenant(BaseModel):
    __tablename__ = "tenants"

    id: int | None = None
    name: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


engine.register_model(Tenant.__tablename__, Tenant)
