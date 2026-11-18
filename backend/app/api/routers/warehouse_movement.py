"""
Warehouse movement API router.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.warehouse.commands.create_movement import CreateMovementCommand
from app.application.warehouse.exceptions import (
    StockNotFoundApplicationError,
    UnsupportedWarehouseMovementApplicationError,
)
from app.application.warehouse.queries.warehouse_movement_read_service import (
    WarehouseMovementReadService,
)
from app.application.warehouse.services.warehouse_application_service import (
    WarehouseApplicationService,
)
from app.core.dependencies.services import (
    get_warehouse_movement_read_service,
    get_warehouse_service,
)
from app.domains.user.entities.user import User
from app.domains.warehouse.exceptions import WarehouseException
from app.domains.warehouse.value_objects.movement_type import MovementType
from app.schemas.warehouse_movement_read import WarehouseMovementPageRead
from app.schemas.warehouse_movement import (
    WarehouseMovementCreate,
    WarehouseMovementRead,
)

router = APIRouter(prefix="/warehouse-movements", tags=["Warehouse Movements"])


@router.post(
    "/",
    response_model=WarehouseMovementRead,
    status_code=201,
    dependencies=[Depends(require_csrf)],
)
def create_movement(
    data: WarehouseMovementCreate,
    user: User = Depends(get_current_user),
    service: WarehouseApplicationService = Depends(get_warehouse_service),
):
    try:
        return service.create_movement(
            CreateMovementCommand(
                warehouse_id=data.warehouse_id,
                material_id=data.material_id,
                movement_type=data.movement_type,
                quantity=data.quantity,
                order_id=data.order_id,
                comment=data.comment,
            ),
            user,
        )
    except StockNotFoundApplicationError:
        raise HTTPException(status_code=404, detail="Stock not found") from None
    except UnsupportedWarehouseMovementApplicationError:
        raise HTTPException(
            status_code=400,
            detail="Unsupported warehouse movement type",
        ) from None
    except WarehouseException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None



@router.get(
    "/warehouse/{warehouse_id}",
    response_model=WarehouseMovementPageRead,
)
def list_warehouse_movements(
    warehouse_id: UUID,
    material_id: UUID | None = Query(default=None),
    order_id: UUID | None = Query(default=None),
    movement_type: MovementType | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: WarehouseMovementReadService = Depends(
        get_warehouse_movement_read_service,
    ),
) -> WarehouseMovementPageRead:
    """List warehouse movement history with optional filters."""
    if date_from is not None and date_to is not None and date_from > date_to:
        raise HTTPException(
            status_code=422,
            detail="date_from must not be later than date_to",
        )

    items, total = service.list_by_warehouse(
        warehouse_id,
        material_id=material_id,
        order_id=order_id,
        movement_type=movement_type,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )
    return WarehouseMovementPageRead(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )
