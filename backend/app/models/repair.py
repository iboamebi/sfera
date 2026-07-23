import uuid
from enum import StrEnum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class RepairStatus(StrEnum):
    NEW = "NEW"
    IN_WORK = "IN_WORK"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Repair(BaseModel):
    __tablename__ = "repairs"

    order_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("order_items.id"),
        nullable=False,
    )

    status: Mapped[RepairStatus] = mapped_column(
        SqlEnum(RepairStatus),
        default=RepairStatus.NEW,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    order_item = relationship(
        "OrderItem",
        back_populates="repairs",
    )
