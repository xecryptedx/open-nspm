from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ..core.db import BaseModel, engine


@dataclass
class Snapshot(BaseModel):
    __tablename__ = "snapshots"

    id: int | None = None
    device_id: int = 0
    taken_at: datetime = field(default_factory=datetime.utcnow)
    source: str = "upload"
    raw_blob: str | None = None
    normalized_json: dict | None = field(default_factory=dict)


engine.register_model(Snapshot.__tablename__, Snapshot)
