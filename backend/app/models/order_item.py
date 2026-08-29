import uuid

from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class OrderItem(BaseModel):
    """Persist one order position and its requested operations."""

    __tablename__ = "order_items"

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )

    instrument_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("instruments.id"),
        nullable=True,
    )

    instrument_type_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("instrument_types.id"),
        nullable=True,
    )

    line_number: Mapped[int] = mapped_column(
        nullable=False,
    )

    customer_inventory_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    customer_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    requested_operations: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    order = relationship(
        "Order",
        back_populates="order_items",
    )

    instrument = relationship(
        "Instrument",
    )

    instrument_type = relationship(
        "InstrumentType",
    )

    verifications = relationship(
        "Verification",
        back_populates="order_item",
        cascade="all, delete-orphan",
    )

    diagnostics = relationship(
        "Diagnostic",
        back_populates="order_item",
        cascade="all, delete-orphan",
    )

    repairs = relationship(
        "Repair",
        back_populates="order_item",
        cascade="all, delete-orphan",
    )
