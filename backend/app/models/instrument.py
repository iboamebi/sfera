import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Instrument(BaseModel):
    """ORM model for an individual measuring instrument."""

    __tablename__ = "instruments"

    instrument_type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("instrument_types.id"),
        nullable=False,
    )

    name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    serial_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    device_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="AVAILABLE",
        server_default="AVAILABLE",
    )

    registry_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    modification: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    factory_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    manufacture_year: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    inventory_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    instrument_type = relationship(
        "InstrumentType",
        back_populates="instruments",
    )
