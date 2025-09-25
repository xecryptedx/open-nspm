from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from ..core.db import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    vendor: Mapped[str] = mapped_column(String(64), default="fortinet", nullable=False)
    hostname: Mapped[str] = mapped_column(String(255), nullable=False)
    mgmt_ip: Mapped[str] = mapped_column(String(64), nullable=True)
    api_url: Mapped[str] = mapped_column(String(512), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="devices")
    snapshots: Mapped[list["Snapshot"]] = relationship(
        "Snapshot", back_populates="device", cascade="all, delete-orphan"
    )
