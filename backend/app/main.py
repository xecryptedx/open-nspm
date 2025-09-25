from __future__ import annotations

from fastapi import FastAPI

from .api.v1 import api_router
from .core import db, logging as logging_config


logging_config.configure_logging()

app = FastAPI(title="OpenNSPM", version="0.1.0")
app.include_router(api_router)


@app.on_event("startup")
def on_startup() -> None:
    db.Base.metadata.create_all(bind=db.engine)


@app.get("/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
