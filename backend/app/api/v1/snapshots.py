from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile

from ... import models
from ...core.db import SessionLocal
from ...core.security import require_api_key
from ...importers import fortigate_text
from ...services.normalizer import normalize_fortigate_payload

router = APIRouter(prefix="/v1/snapshots", tags=["snapshots"], dependencies=[require_api_key])


@router.post(":upload", status_code=201)
def upload_snapshot(device_id: int, file: UploadFile) -> dict:
    session = SessionLocal()
    device = session.get(models.Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    raw_text = file.read().decode()
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
    session.add(snapshot)
    session.commit()
    session.refresh(snapshot)
    return snapshot.to_dict()


@router.get("")
def list_snapshots(device_id: int | None = None) -> list[dict]:
    session = SessionLocal()
    query = session.query(models.Snapshot)
    if device_id:
        query = query.filter(lambda item: item.device_id == device_id)
    snapshots = query.order_by(lambda item: item.taken_at, reverse=True).all()
    return [snap.to_dict() for snap in snapshots]


@router.get("/{snapshot_id}")
def get_snapshot(snapshot_id: int) -> dict:
    session = SessionLocal()
    snapshot = session.get(models.Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return snapshot.to_dict()
