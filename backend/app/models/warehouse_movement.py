import uuid
from enum import StrEnum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class MovementType(StrEnum):
    RECEIPT = "RECEIPT"
    ISSUE = "ISSUE"
    RESERVATION = "RESERVATION"
    RELEASE = "RELEASE"
    ADJUSTMENT = "ADJUSTMENT"


class WarehouseMovement(BaseModel):
    __tablename__ = "warehouse_movements"

    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    material_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("materials.id"),
        nullable=False,
    )

    order_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("orders.id"),
        nullable=True,
    )

    movement_type: Mapped[MovementType] = mapped_column(
        SqlEnum(MovementType),
        nullable=False,
    )

    quantity: Mapped[float] = mapped_column(
        Numeric(12, 3),
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
