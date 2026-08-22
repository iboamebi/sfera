from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class InstrumentType(BaseModel):
    __tablename__ = "instrument_types"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    model: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    measurement_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    accuracy_class: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    verification_interval_months: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    instruments = relationship(
        "Instrument",
    )
