from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ... import models
from ...core.db import SessionLocal
from ...core.security import require_api_key
from ...services.hygiene import run_hygiene

router = APIRouter(prefix="/v1/findings", tags=["findings"], dependencies=[require_api_key])


@router.post(":run")
def run_findings(payload: dict) -> list[dict]:
    session = SessionLocal()
    snapshot = session.get(models.Snapshot, payload.get("snapshot_id", 0))
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    checks = payload.get("checks") or []
    findings_payload = run_hygiene(snapshot.normalized_json or {}, checks)

    created: list[models.Finding] = []
    for item in findings_payload:
        finding = models.Finding(
            snapshot_id=snapshot.id,
            type=item.get("type", "unknown"),
            severity=item.get("severity", "low"),
            summary=item.get("summary", ""),
            details=item.get("details", {}),
            rule_ids=item.get("rule_ids") or [],
        )
        session.add(finding)
        created.append(finding)
    session.commit()
    return [f.to_dict() for f in created]


@router.get("")
def list_findings(snapshot_id: int | None = None) -> list[dict]:
    session = SessionLocal()
    query = session.query(models.Finding)
    if snapshot_id:
        query = query.filter(lambda item: item.snapshot_id == snapshot_id)
    findings = query.order_by(lambda item: item.created_at, reverse=True).all()
    return [finding.to_dict() for finding in findings]
