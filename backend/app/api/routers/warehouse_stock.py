"""
Warehouse stock API router.
"""

from fastapi import APIRouter, Depends

from app.application.warehouse.commands.add_stock import (
    AddStockCommand,
)
from app.application.warehouse.services.warehouse_application_service import (
    WarehouseApplicationService,
)
from app.core.dependencies.services import (
    get_warehouse_service,
)
from app.schemas.warehouse_stock import (
    WarehouseStockCreate,
    WarehouseStockRead,
)

router = APIRouter(
    prefix="/warehouse-stocks",
    tags=["Warehouse Stocks"],
)


@router.post(
    "/",
    response_model=WarehouseStockRead,
    status_code=201,
)
def add_stock(
    data: WarehouseStockCreate,
    service: WarehouseApplicationService = Depends(
        get_warehouse_service,
    ),
):
    return service.add_stock(
        AddStockCommand(
            warehouse_id=data.warehouse_id,
            material_id=data.material_id,
            quantity=data.quantity,
        )
    )
