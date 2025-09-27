from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ... import models
from ...core.db import SessionLocal
from ...core.security import require_api_key
from ...services.diff_engine import compute_diff

router = APIRouter(prefix="/v1/diffs", tags=["diffs"], dependencies=[require_api_key])


@router.post("", status_code=201)
def create_diff(payload: dict) -> dict:
    session = SessionLocal()
    base = session.get(models.Snapshot, payload.get("base_snapshot_id", 0))
    head = session.get(models.Snapshot, payload.get("head_snapshot_id", 0))
    if not base or not head:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    diff_payload = compute_diff(base.normalized_json or {}, head.normalized_json or {})
    diff = models.Diff(
        base_snapshot_id=base.id,
        head_snapshot_id=head.id,
        summary=diff_payload["summary"],
        details=diff_payload["details"],
    )
    session.add(diff)
    session.commit()
    session.refresh(diff)
    return diff.to_dict()


@router.get("/{diff_id}")
def get_diff(diff_id: int) -> dict:
    session = SessionLocal()
    diff = session.get(models.Diff, diff_id)
    if not diff:
        raise HTTPException(status_code=404, detail="Diff not found")
    return diff.to_dict()
