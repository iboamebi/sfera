"""
Warehouse stock API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.warehouse.commands.add_stock import AddStockCommand
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
from app.domains.user.entities.user import User
from app.domains.warehouse.exceptions import WarehouseException
from app.schemas.warehouse_stock import WarehouseStockCreate, WarehouseStockRead
from app.schemas.warehouse_stock_read import (
    WarehouseStockRead as WarehouseStockReadSchema,
)

router = APIRouter(prefix="/warehouse-stocks", tags=["Warehouse Stocks"])


@router.post(
    "/",
    response_model=WarehouseStockRead,
    status_code=201,
    dependencies=[Depends(require_csrf)],
)
def add_stock(
    data: WarehouseStockCreate,
    user: User = Depends(get_current_user),
    service: WarehouseApplicationService = Depends(get_warehouse_service),
):
    try:
        return service.add_stock(
            AddStockCommand(
                warehouse_id=data.warehouse_id,
                material_id=data.material_id,
                quantity=data.quantity,
            ),
            user,
        )
    except WarehouseException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None


@router.get(
    "/warehouse/{warehouse_id}",
    response_model=list[WarehouseStockReadSchema],
)
def get_warehouse_stock(
    warehouse_id: UUID,
    service: WarehouseStockReadService = Depends(get_warehouse_stock_read_service),
):
    return service.get_by_warehouse(warehouse_id)
