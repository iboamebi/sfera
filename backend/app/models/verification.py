import uuid
from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import Date, DateTime, ForeignKey, Index, String, Text, text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class VerificationResult(StrEnum):
    SUITABLE = "SUITABLE"
    UNSUITABLE = "UNSUITABLE"


class VerificationStatus(StrEnum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    DECIDED = "DECIDED"
    CANCELLED = "CANCELLED"


class VerificationType(StrEnum):
    PRIMARY = "PRIMARY"
    PERIODIC = "PERIODIC"
    AFTER_REPAIR = "AFTER_REPAIR"


class Verification(BaseModel):
    """ORM model for an instrument verification process."""

    __tablename__ = "verifications"
    __table_args__ = (
        Index(
            "uq_verifications_one_active_per_order_item",
            "order_item_id",
            unique=True,
            postgresql_where=text(
                "archived = false AND status IN ('CREATED', 'IN_PROGRESS')"
            ),
        ),
    )

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

    status: Mapped[VerificationStatus] = mapped_column(
        SqlEnum(VerificationStatus, name="verification_status"),
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    decision_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    valid_until: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    result: Mapped[VerificationResult | None] = mapped_column(
        SqlEnum(VerificationResult),
        nullable=True,
    )

    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    unsuitable_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    methodology: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    verification_type: Mapped[VerificationType] = mapped_column(
        SqlEnum(VerificationType, name="verification_type"),
        nullable=False,
    )

    order_item = relationship(
        "OrderItem",
        back_populates="verifications",
    )
