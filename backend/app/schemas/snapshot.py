from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .common import ORMBase


@dataclass
class SnapshotRead(ORMBase):
    id: int
    device_id: int
    taken_at: datetime
    source: str
    normalized_json: dict
    hash: str | None = None
