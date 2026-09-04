import uuid
from datetime import date
from enum import StrEnum

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class VerificationResult(StrEnum):
    SUITABLE = "SUITABLE"
    UNSUITABLE = "UNSUITABLE"


class Verification(BaseModel):
    """ORM model for an instrument verification result."""

    __tablename__ = "verifications"

    order_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("order_items.id"),
        nullable=False,
    )

    instrument_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("instruments.id"),
        nullable=True,
    )

    verification_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    valid_until: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    result: Mapped[VerificationResult] = mapped_column(
        SqlEnum(VerificationResult),
        nullable=False,
    )

    unsuitable_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    methodology: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    order_item = relationship(
        "OrderItem",
        back_populates="verifications",
    )
