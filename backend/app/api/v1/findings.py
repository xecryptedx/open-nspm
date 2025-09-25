from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ... import models, schemas
from ...core.db import get_db
from ...core.security import api_key_dependency
from ...services.hygiene import run_hygiene

router = APIRouter(prefix="/v1/findings", tags=["findings"], dependencies=[Depends(api_key_dependency)])


@router.post(":run", response_model=list[schemas.FindingRead])
def run_findings(request: schemas.FindingRunRequest, db: Session = Depends(get_db)):
    snapshot = db.get(models.Snapshot, request.snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    findings_payload = run_hygiene(snapshot.normalized_json or {}, request.checks)

    created: list[models.Finding] = []
    for item in findings_payload:
        finding = models.Finding(
            snapshot_id=snapshot.id,
            type=item.get("type", "unknown"),
            severity=item.get("severity", "low"),
            summary=item.get("summary", ""),
            details=item.get("details", {}),
            rule_ids=item.get("rule_ids"),
        )
        db.add(finding)
        created.append(finding)
    db.commit()
    for finding in created:
        db.refresh(finding)
    return created


@router.get("", response_model=list[schemas.FindingRead])
def list_findings(snapshot_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Finding)
    if snapshot_id:
        query = query.filter(models.Finding.snapshot_id == snapshot_id)
    return query.order_by(models.Finding.created_at.desc()).all()
