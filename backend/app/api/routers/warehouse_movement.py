"""
Warehouse movement API router.
"""

from fastapi import APIRouter, Depends

from app.application.warehouse.commands.create_movement import (
    CreateMovementCommand,
)
from app.application.warehouse.services.warehouse_application_service import (
    WarehouseApplicationService,
)
from app.core.dependencies.services import (
    get_warehouse_service,
)
from app.schemas.warehouse_movement import (
    WarehouseMovementCreate,
    WarehouseMovementRead,
)

router = APIRouter(
    prefix="/warehouse-movements",
    tags=["Warehouse Movements"],
)


@router.post(
    "/",
    response_model=WarehouseMovementRead,
    status_code=201,
)
def create_movement(
    data: WarehouseMovementCreate,
    service: WarehouseApplicationService = Depends(
        get_warehouse_service,
    ),
):
    return service.create_movement(
        CreateMovementCommand(
            warehouse_id=data.warehouse_id,
            material_id=data.material_id,
            movement_type=data.movement_type,
            quantity=data.quantity,
            order_id=data.order_id,
            comment=data.comment,
        )
    )
