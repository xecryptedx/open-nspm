from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ... import models
from ...core.db import get_db
from ...core.security import api_key_dependency
from ...reports.html import render_html_report

router = APIRouter(prefix="/v1/reports", tags=["reports"], dependencies=[Depends(api_key_dependency)])


@router.get("/{snapshot_id}.html", response_class=HTMLResponse)
def get_html_report(snapshot_id: int, db: Session = Depends(get_db)):
    snapshot = db.get(models.Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    findings = db.query(models.Finding).filter(models.Finding.snapshot_id == snapshot_id).all()
    diff = (
        db.query(models.Diff)
        .filter(models.Diff.head_snapshot_id == snapshot_id)
        .order_by(models.Diff.created_at.desc())
        .first()
    )

    snapshot_dict = {
        "id": snapshot.id,
        "taken_at": snapshot.taken_at.isoformat(),
        "normalized_json": snapshot.normalized_json or {},
        "device": {
            "id": snapshot.device.id if snapshot.device else None,
            "hostname": snapshot.device.hostname if snapshot.device else None,
        },
    }
    findings_payload = [
        {
            "type": f.type,
            "severity": f.severity,
            "summary": f.summary,
        }
        for f in findings
    ]
    diff_payload = {
        "summary": diff.summary if diff else {},
        "details": diff.details if diff else {},
    }
    html = render_html_report(snapshot_dict, findings_payload, diff_payload)
    return HTMLResponse(content=html)
