from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from ..core.db import Base


class Snapshot(Base):
    __tablename__ = "snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False, index=True)
    taken_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    source: Mapped[str] = mapped_column(String(32), default="upload", nullable=False)
    raw_blob: Mapped[str] = mapped_column(Text, nullable=True)
    normalized_json: Mapped[dict] = mapped_column(JSON, default=dict)
    hash: Mapped[str | None] = mapped_column(String(128), nullable=True)

    device: Mapped["Device"] = relationship("Device", back_populates="snapshots")
    findings: Mapped[list["Finding"]] = relationship(
        "Finding", back_populates="snapshot", cascade="all, delete-orphan"
    )
    base_diffs: Mapped[list["Diff"]] = relationship(
        "Diff",
        back_populates="base_snapshot",
        foreign_keys="Diff.base_snapshot_id",
    )
    head_diffs: Mapped[list["Diff"]] = relationship(
        "Diff",
        back_populates="head_snapshot",
        foreign_keys="Diff.head_snapshot_id",
    )
