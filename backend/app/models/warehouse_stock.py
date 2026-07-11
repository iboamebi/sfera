import uuid

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class WarehouseStock(BaseModel):
    __tablename__ = "warehouse_stocks"

    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    material_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("materials.id"),
        nullable=False,
    )

    quantity: Mapped[float] = mapped_column(
        Numeric(12, 3),
        nullable=False,
        default=0,
    )

    reserved_quantity: Mapped[float] = mapped_column(
        Numeric(12, 3),
        nullable=False,
        default=0,
    )
