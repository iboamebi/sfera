from app.api.base_router import BaseRouter
from app.crud.warehouse_movement import warehouse_movement_crud
from app.schemas.warehouse_movement import (
    WarehouseMovementCreate,
    WarehouseMovementRead,
    WarehouseMovementUpdate,
)

router = BaseRouter(
    crud=warehouse_movement_crud,
    read_schema=WarehouseMovementRead,
    create_schema=WarehouseMovementCreate,
    update_schema=WarehouseMovementUpdate,
    prefix="/warehouse-movements",
    tags=["Warehouse Movements"],
).router
