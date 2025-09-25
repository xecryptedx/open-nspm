from fastapi import APIRouter

from . import devices, snapshots, findings, diffs, reports

api_router = APIRouter()
api_router.include_router(devices.router)
api_router.include_router(snapshots.router)
api_router.include_router(findings.router)
api_router.include_router(diffs.router)
api_router.include_router(reports.router)
