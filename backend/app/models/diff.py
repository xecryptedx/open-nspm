from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ..core.db import BaseModel, engine


@dataclass
class Diff(BaseModel):
    __tablename__ = "diffs"

    id: int | None = None
    base_snapshot_id: int = 0
    head_snapshot_id: int = 0
    summary: dict = field(default_factory=dict)
    details: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


engine.register_model(Diff.__tablename__, Diff)
