from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ..core.db import BaseModel, engine


@dataclass
class Finding(BaseModel):
    __tablename__ = "findings"

    id: int | None = None
    snapshot_id: int = 0
    type: str = "unknown"
    severity: str = "low"
    summary: str = ""
    details: dict | None = field(default_factory=dict)
    rule_ids: list[int] | None = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)


engine.register_model(Finding.__tablename__, Finding)
