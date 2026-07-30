"""
Repair API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.repair.commands.create_repair import (
    CreateRepairCommand,
)
from app.application.repair.services.repair_application_service import (
    RepairApplicationService,
)
from app.core.dependencies.services import get_repair_service
from app.schemas.repair import (
    RepairComplete,
    RepairCreate,
    RepairRead,
)

router = APIRouter(
    prefix="/repairs",
    tags=["Repairs"],
)


@router.get(
    "/{repair_id}",
    response_model=RepairRead,
)
def get_repair(
    repair_id: UUID,
    service: RepairApplicationService = Depends(
        get_repair_service,
    ),
):
    try:
        return service.get(
            repair_id,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Repair not found",
        ) from None


@router.post(
    "",
    response_model=RepairRead,
)
def create_repair(
    data: RepairCreate,
    service: RepairApplicationService = Depends(
        get_repair_service,
    ),
):
    return service.create(
        CreateRepairCommand(
            order_item_id=data.order_item_id,
            description=data.description,
        ),
    )


@router.post(
    "/{repair_id}/start",
    response_model=RepairRead,
)
def start_repair(
    repair_id: UUID,
    service: RepairApplicationService = Depends(
        get_repair_service,
    ),
):
    return service.start(
        repair_id,
    )


@router.post(
    "/{repair_id}/complete",
    response_model=RepairRead,
)
def complete_repair(
    repair_id: UUID,
    data: RepairComplete,
    service: RepairApplicationService = Depends(
        get_repair_service,
    ),
):
    return service.complete(
        repair_id,
        data.result,
    )


@router.post(
    "/{repair_id}/cancel",
    response_model=RepairRead,
)
def cancel_repair(
    repair_id: UUID,
    service: RepairApplicationService = Depends(
        get_repair_service,
    ),
):
    return service.cancel(
        repair_id,
    )
