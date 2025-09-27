from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ... import models
from ...core.db import SessionLocal
from ...core.security import require_api_key

router = APIRouter(prefix="/v1/devices", tags=["devices"], dependencies=[require_api_key])


@router.post("", status_code=201)
def create_device(payload: dict) -> dict:
    session = SessionLocal()
    tenant = session.get(models.Tenant, payload.get("tenant_id", 0))
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    device = models.Device(
        tenant_id=payload["tenant_id"],
        vendor=payload.get("vendor", "fortinet"),
        hostname=payload["hostname"],
        mgmt_ip=payload.get("mgmt_ip"),
        api_url=payload.get("api_url"),
        metadata=payload.get("metadata") or {},
    )
    session.add(device)
    session.commit()
    session.refresh(device)
    return device.to_dict()


@router.get("")
def list_devices() -> list[dict]:
    session = SessionLocal()
    return [device.to_dict() for device in session.query(models.Device).all()]


@router.get("/{device_id}")
def get_device(device_id: int) -> dict:
    session = SessionLocal()
    device = session.get(models.Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device.to_dict()
