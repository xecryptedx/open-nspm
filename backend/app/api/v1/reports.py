from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from ... import models
from ...core.db import SessionLocal
from ...core.security import require_api_key
from ...reports.html import render_html_report

router = APIRouter(prefix="/v1/reports", tags=["reports"], dependencies=[require_api_key])


@router.get("/{snapshot_id}.html", response_class=HTMLResponse)
def get_html_report(snapshot_id: int) -> HTMLResponse:
    session = SessionLocal()
    snapshot = session.get(models.Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    findings = session.query(models.Finding).filter(lambda f: f.snapshot_id == snapshot_id).all()
    diffs = session.query(models.Diff).filter(lambda d: d.head_snapshot_id == snapshot_id)
    diff = diffs.order_by(lambda d: d.created_at, reverse=True).first()

    snapshot_payload = {
        "id": snapshot.id,
        "taken_at": snapshot.taken_at.isoformat(),
        "normalized_json": snapshot.normalized_json or {},
        "device": {"id": snapshot.device_id},
    }
    findings_payload = [
        {"type": item.type, "severity": item.severity, "summary": item.summary}
        for item in findings
    ]
    diff_payload = {
        "summary": diff.summary if diff else {},
        "details": diff.details if diff else {},
    }
    html = render_html_report(snapshot_payload, findings_payload, diff_payload)
    return HTMLResponse(content=html)
