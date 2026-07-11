from app.crud.base import BaseCRUD
from app.models.warehouse_stock import WarehouseStock
from app.schemas.warehouse_stock import (
    WarehouseStockCreate,
    WarehouseStockUpdate,
)


class WarehouseStockCRUD(
    BaseCRUD[
        WarehouseStock,
        WarehouseStockCreate,
        WarehouseStockUpdate,
    ]
):
    pass


warehouse_stock_crud = WarehouseStockCRUD(WarehouseStock)
