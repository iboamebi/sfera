from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WarehouseStockBase(BaseModel):
    warehouse_id: UUID
    material_id: UUID
    quantity: float = 0
    reserved_quantity: float = 0


class WarehouseStockCreate(WarehouseStockBase):
    pass


class WarehouseStockUpdate(BaseModel):
    quantity: float | None = None
    reserved_quantity: float | None = None


class WarehouseStockRead(WarehouseStockBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
