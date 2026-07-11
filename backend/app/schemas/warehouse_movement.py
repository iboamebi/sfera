from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.warehouse_movement import MovementType


class WarehouseMovementBase(BaseModel):
    warehouse_id: UUID
    material_id: UUID
    order_id: UUID | None = None
    movement_type: MovementType
    quantity: float
    comment: str | None = None


class WarehouseMovementCreate(WarehouseMovementBase):
    pass


class WarehouseMovementUpdate(BaseModel):
    movement_type: MovementType | None = None
    quantity: float | None = None
    comment: str | None = None


class WarehouseMovementRead(WarehouseMovementBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
