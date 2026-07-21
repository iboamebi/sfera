from app.crud.base import BaseCRUD
from app.models.warehouse_movement import WarehouseMovement
from app.schemas.warehouse_movement import (
    WarehouseMovementCreate,
    WarehouseMovementUpdate,
)


class WarehouseMovementCRUD(
    BaseCRUD[
        WarehouseMovement,
        WarehouseMovementCreate,
        WarehouseMovementUpdate,
    ]
):
    pass


warehouse_movement_crud = WarehouseMovementCRUD(WarehouseMovement)
