import uuid
from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class ProductionStage(str, Enum):
    RECEIVED = "RECEIVED"
    REGISTRATION = "REGISTRATION"
    DIAGNOSTIC = "DIAGNOSTIC"
    REPAIR = "REPAIR"
    VERIFICATION = "VERIFICATION"
    QUALITY_CONTROL = "QUALITY_CONTROL"
    ISSUANCE = "ISSUANCE"


class ProductionMovement(BaseModel):
    __tablename__ = "production_movements"

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )

    stage: Mapped[ProductionStage] = mapped_column(
        SqlEnum(ProductionStage),
        nullable=False,
    )

    responsible_user_id: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    order = relationship(
        "Order",
        back_populates="production_movements",
    )
