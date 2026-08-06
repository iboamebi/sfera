# backend/app/api/routers/price_list.py
# PriceList API router

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.price_list.commands.create_price_list import (
    CreatePriceListCommand,
)
from app.application.price_list.commands.update_price_list import (
    UpdatePriceListCommand,
)
from app.application.price_list.exceptions import (
    PriceListNotFoundApplicationError,
)
from app.application.price_list.services.price_list_application_service import (
    PriceListApplicationService,
)
from app.core.dependencies.services import get_price_list_service
from app.schemas.price_list import (
    PriceListCreate,
    PriceListRead,
    PriceListUpdate,
)

router = APIRouter(
    prefix="/price-lists",
    tags=["Price Lists"],
)


@router.get("/", response_model=list[PriceListRead])
async def get_all(
    service: PriceListApplicationService = Depends(
        get_price_list_service,
    ),
):
    return await service.list_price_lists()


@router.get("/{obj_id}", response_model=PriceListRead)
async def get_one(
    obj_id: UUID,
    service: PriceListApplicationService = Depends(
        get_price_list_service,
    ),
):
    obj = await service.get_price_list(obj_id)

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Object not found",
        )

    return obj


@router.post("/", response_model=PriceListRead, status_code=201)
async def create(
    data: PriceListCreate,
    service: PriceListApplicationService = Depends(
        get_price_list_service,
    ),
):
    command = CreatePriceListCommand(
        name=data.name,
        price_list_type=data.price_list_type,
        description=data.description,
    )

    return await service.create(command)


@router.patch("/{obj_id}", response_model=PriceListRead)
async def update(
    obj_id: UUID,
    data: PriceListUpdate,
    service: PriceListApplicationService = Depends(
        get_price_list_service,
    ),
):
    command = UpdatePriceListCommand(
        price_list_id=obj_id,
        name=data.name,
        description=data.description,
    )

    try:
        return await service.update(command)

    except PriceListNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Object not found",
        ) from None
