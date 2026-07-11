from app.api.base_router import BaseRouter
from app.crud.warehouse import warehouse_crud
from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseRead,
    WarehouseUpdate,
)

router = BaseRouter(
    crud=warehouse_crud,
    read_schema=WarehouseRead,
    create_schema=WarehouseCreate,
    update_schema=WarehouseUpdate,
    prefix="/warehouses",
    tags=["Warehouses"],
).router
