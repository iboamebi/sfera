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
from app.application.warehouse.services.warehouse_application_service import (
    WarehouseApplicationService,
)
from app.core.dependencies.services import get_warehouse_service
from app.domains.user.entities.user import User
from app.domains.warehouse.exceptions import WarehouseException
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
