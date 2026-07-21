import uuid
from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class LabelType(str, Enum):
    QR = "QR"
    BARCODE = "BARCODE"
    DATAMATRIX = "DATAMATRIX"


class InstrumentLabel(BaseModel):
    __tablename__ = "instrument_labels"

    instrument_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("instruments.id"),
        nullable=False,
    )

    label_type: Mapped[LabelType] = mapped_column(
        SqlEnum(LabelType),
        nullable=False,
    )

    value: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    replacement_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
