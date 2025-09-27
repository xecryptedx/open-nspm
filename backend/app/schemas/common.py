from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass
class ORMBase:
    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Timestamped(ORMBase):
    created_at: datetime
