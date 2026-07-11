from app.api.base_router import BaseRouter
from app.crud.warehouse_stock import warehouse_stock_crud
from app.schemas.warehouse_stock import (
    WarehouseStockCreate,
    WarehouseStockRead,
    WarehouseStockUpdate,
)

router = BaseRouter(
    crud=warehouse_stock_crud,
    read_schema=WarehouseStockRead,
    create_schema=WarehouseStockCreate,
    update_schema=WarehouseStockUpdate,
    prefix="/warehouse-stocks",
    tags=["Warehouse Stocks"],
).router
