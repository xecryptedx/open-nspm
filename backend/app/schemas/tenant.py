from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .common import ORMBase, Timestamped


@dataclass
class TenantCreate(ORMBase):
    name: str


@dataclass
class TenantRead(Timestamped):
    id: int
    name: str
    created_at: datetime
