"""
Warehouse stock API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.warehouse.commands.add_stock import (
    AddStockCommand,
)
from app.application.warehouse.queries.warehouse_stock_read_service import (
    WarehouseStockReadService,
)
from app.application.warehouse.services.warehouse_application_service import (
    WarehouseApplicationService,
)
from app.core.dependencies.services import (
    get_warehouse_service,
    get_warehouse_stock_read_service,
)
from app.schemas.warehouse_stock import (
    WarehouseStockCreate,
    WarehouseStockRead,
)
from app.schemas.warehouse_stock_read import (
    WarehouseStockRead as WarehouseStockReadSchema,
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


@router.get(
    "/warehouse/{warehouse_id}",
    response_model=list[WarehouseStockReadSchema],
)
def get_warehouse_stock(
    warehouse_id: UUID,
    service: WarehouseStockReadService = Depends(
        get_warehouse_stock_read_service,
    ),
):
    return service.get_by_warehouse(
        warehouse_id,
    )
