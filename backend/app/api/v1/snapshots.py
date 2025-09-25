from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ... import models, schemas
from ...core.db import get_db
from ...core.security import api_key_dependency
from ...importers import fortigate_text
from ...services.normalizer import normalize_fortigate_payload

router = APIRouter(prefix="/v1/snapshots", tags=["snapshots"], dependencies=[Depends(api_key_dependency)])


@router.post(":upload", response_model=schemas.SnapshotRead, status_code=status.HTTP_201_CREATED)
async def upload_snapshot(
    device_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    device = db.get(models.Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    raw_text = (await file.read()).decode()
    parsed = fortigate_text.parse(raw_text)
    parsed.setdefault("services", [])
    normalized = normalize_fortigate_payload(parsed)

    snapshot = models.Snapshot(
        device_id=device_id,
        taken_at=datetime.utcnow(),
        source="upload",
        raw_blob=raw_text,
        normalized_json=normalized,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot


@router.get("", response_model=list[schemas.SnapshotRead])
async def list_snapshots(device_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Snapshot)
    if device_id:
        query = query.filter(models.Snapshot.device_id == device_id)
    return query.order_by(models.Snapshot.taken_at.desc()).all()


@router.get("/{snapshot_id}", response_model=schemas.SnapshotRead)
async def get_snapshot(snapshot_id: int, db: Session = Depends(get_db)):
    snapshot = db.get(models.Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return snapshot
