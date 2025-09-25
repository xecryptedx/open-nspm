from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ... import models, schemas
from ...core.db import get_db
from ...core.security import api_key_dependency
from ...services.diff_engine import compute_diff

router = APIRouter(prefix="/v1/diffs", tags=["diffs"], dependencies=[Depends(api_key_dependency)])


@router.post("", response_model=schemas.DiffRead, status_code=status.HTTP_201_CREATED)
def create_diff(request: schemas.DiffCreate, db: Session = Depends(get_db)):
    base = db.get(models.Snapshot, request.base_snapshot_id)
    head = db.get(models.Snapshot, request.head_snapshot_id)
    if not base or not head:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    diff_payload = compute_diff(base.normalized_json or {}, head.normalized_json or {})
    diff = models.Diff(
        base_snapshot_id=base.id,
        head_snapshot_id=head.id,
        summary=diff_payload["summary"],
        details=diff_payload["details"],
    )
    db.add(diff)
    db.commit()
    db.refresh(diff)
    return diff


@router.get("/{diff_id}", response_model=schemas.DiffRead)
def get_diff(diff_id: int, db: Session = Depends(get_db)):
    diff = db.get(models.Diff, diff_id)
    if not diff:
        raise HTTPException(status_code=404, detail="Diff not found")
    return diff
