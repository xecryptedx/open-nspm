from datetime import datetime

from pydantic import Field

from .common import ORMBase


class FindingRunRequest(ORMBase):
    snapshot_id: int
    checks: list[str] = Field(default_factory=list)


class FindingCreate(ORMBase):
    snapshot_id: int
    type: str
    severity: str
    summary: str
    details: dict
    rule_ids: list[int] | None = None


class FindingRead(ORMBase):
    id: int
    snapshot_id: int
    type: str
    severity: str
    summary: str
    details: dict
    rule_ids: list[int] | None
    created_at: datetime
