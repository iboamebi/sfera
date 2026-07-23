import uuid
from enum import StrEnum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Recommendation(StrEnum):
    NO_ISSUES = "NO_ISSUES"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    REPLACEMENT_RECOMMENDED = "REPLACEMENT_RECOMMENDED"
    REPAIR_NOT_ECONOMIC = "REPAIR_NOT_ECONOMIC"
    WRITE_OFF = "WRITE_OFF"
    RETURN_TO_MANUFACTURER = "RETURN_TO_MANUFACTURER"


class Diagnostic(BaseModel):
    __tablename__ = "diagnostics"

    order_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("order_items.id"),
        nullable=False,
    )

    conclusion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    recommendation: Mapped[Recommendation | None] = mapped_column(
        SqlEnum(Recommendation),
        nullable=True,
    )

    order_item = relationship(
        "OrderItem",
    )
