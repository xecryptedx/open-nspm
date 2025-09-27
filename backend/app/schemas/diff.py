from __future__ import annotations

from dataclasses import dataclass

from .common import ORMBase


@dataclass
class DiffCreate(ORMBase):
    base_snapshot_id: int
    head_snapshot_id: int


@dataclass
class DiffRead(ORMBase):
    id: int
    base_snapshot_id: int
    head_snapshot_id: int
    summary: dict
    details: dict
