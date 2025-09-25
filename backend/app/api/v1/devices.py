from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ... import models, schemas
from ...core.db import get_db
from ...core.security import api_key_dependency

router = APIRouter(prefix="/v1/devices", tags=["devices"], dependencies=[Depends(api_key_dependency)])


@router.post("", response_model=schemas.DeviceRead, status_code=status.HTTP_201_CREATED)
def create_device(device_in: schemas.DeviceCreate, db: Session = Depends(get_db)):
    tenant = db.get(models.Tenant, device_in.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    device = models.Device(**device_in.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.get("", response_model=list[schemas.DeviceRead])
def list_devices(db: Session = Depends(get_db)):
    return db.query(models.Device).all()


@router.get("/{device_id}", response_model=schemas.DeviceRead)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.get(models.Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device
