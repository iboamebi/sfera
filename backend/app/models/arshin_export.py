import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class ArshinExport(BaseModel):
    __tablename__ = "arshin_exports"

    verification_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("verifications.id"),
        nullable=False,
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    exported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    exported_by: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
