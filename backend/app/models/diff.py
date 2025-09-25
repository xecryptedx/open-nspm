from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from ..core.db import Base


class Diff(Base):
    __tablename__ = "diffs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    base_snapshot_id: Mapped[int] = mapped_column(ForeignKey("snapshots.id"), nullable=False)
    head_snapshot_id: Mapped[int] = mapped_column(ForeignKey("snapshots.id"), nullable=False)
    summary: Mapped[dict] = mapped_column(JSON, default=dict)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    base_snapshot: Mapped["Snapshot"] = relationship(
        "Snapshot", back_populates="base_diffs", foreign_keys=[base_snapshot_id]
    )
    head_snapshot: Mapped["Snapshot"] = relationship(
        "Snapshot", back_populates="head_diffs", foreign_keys=[head_snapshot_id]
    )
