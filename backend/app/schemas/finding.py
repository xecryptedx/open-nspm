from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .common import ORMBase, Timestamped


@dataclass
class FindingCreate(ORMBase):
    snapshot_id: int
    type: str
    severity: str
    summary: str
    details: dict | None = None
    rule_ids: list[int] | None = None


@dataclass
class FindingRead(Timestamped):
    id: int
    snapshot_id: int
    type: str
    severity: str
    summary: str
    details: dict | None
    rule_ids: list[int] | None
    created_at: datetime


@dataclass
class FindingRunRequest(ORMBase):
    snapshot_id: int
    checks: list[str]
