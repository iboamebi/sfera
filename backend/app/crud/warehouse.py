from app.crud.base import BaseCRUD
from app.models.warehouse import Warehouse
from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseUpdate,
)


class WarehouseCRUD(
    BaseCRUD[
        Warehouse,
        WarehouseCreate,
        WarehouseUpdate,
    ]
):
    pass


warehouse_crud = WarehouseCRUD(Warehouse)
