from datetime import datetime

from .common import ORMBase


class SnapshotRead(ORMBase):
    id: int
    device_id: int
    taken_at: datetime
    source: str
    normalized_json: dict
    hash: str | None = None
