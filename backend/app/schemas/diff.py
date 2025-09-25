from datetime import datetime

from .common import ORMBase


class DiffCreate(ORMBase):
    base_snapshot_id: int
    head_snapshot_id: int


class DiffRead(ORMBase):
    id: int
    base_snapshot_id: int
    head_snapshot_id: int
    summary: dict
    details: dict
    created_at: datetime
