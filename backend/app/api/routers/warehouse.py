"""
Warehouse API router.
"""

from fastapi import APIRouter, Depends

from app.application.warehouse.commands.create_warehouse import (
    CreateWarehouseCommand,
)
from app.application.warehouse.services.warehouse_application_service import (
    WarehouseApplicationService,
)
from app.core.dependencies.services import (
    get_warehouse_service,
)
from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseRead,
)

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"],
)


@router.post(
    "/",
    response_model=WarehouseRead,
    status_code=201,
)
def create_warehouse(
    data: WarehouseCreate,
    service: WarehouseApplicationService = Depends(
        get_warehouse_service,
    ),
):
    return service.create(
        CreateWarehouseCommand(
            name=data.name,
            address=data.address,
            responsible_person=data.responsible_person,
            comment=data.comment,
        )
    )
