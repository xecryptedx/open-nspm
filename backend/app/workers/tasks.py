from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from .. import models
from ..core.db import SessionLocal
from ..services.normalizer import normalize_fortigate_payload


def pull_snapshot_task(device_id: int, payload: dict[str, Any]) -> int:
    """Persist a snapshot from an already collected FortiGate payload."""
    normalized = normalize_fortigate_payload(payload)
    with SessionLocal() as session:
        snapshot = models.Snapshot(
            device_id=device_id,
            taken_at=datetime.utcnow(),
            source="api",
            normalized_json=normalized,
        )
        session.add(snapshot)
        session.commit()
        session.refresh(snapshot)
        return snapshot.id
