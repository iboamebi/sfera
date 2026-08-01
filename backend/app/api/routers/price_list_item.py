"""
PriceListItem API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.price_list.commands.add_price_list_item import (
    AddPriceListItemCommand,
)
from app.application.price_list.commands.remove_price_list_item import (
    RemovePriceListItemCommand,
)
from app.application.price_list.commands.update_price_list_item import (
    UpdatePriceListItemCommand,
)
from app.application.price_list.services.price_list_application_service import (
    PriceListApplicationService,
)
from app.core.dependencies.services import get_price_list_service
from app.schemas.price_list_item import (
    PriceListItemCreate,
    PriceListItemUpdate,
)

router = APIRouter(
    prefix="/price-list-items",
    tags=["Price List Items"],
)


@router.post(
    "/",
)
async def create(
    data: PriceListItemCreate,
    service: PriceListApplicationService = Depends(
        get_price_list_service,
    ),
):
    return await service.add_item(
        AddPriceListItemCommand(
            price_list_id=data.price_list_id,
            service_code=data.service_type or "",
            name=data.name,
            price=data.unit_price,
        )
    )


@router.patch(
    "/{item_id}",
)
async def update(
    item_id: UUID,
    data: PriceListItemUpdate,
    service: PriceListApplicationService = Depends(
        get_price_list_service,
    ),
):
    try:
        return await service.update_item(
            UpdatePriceListItemCommand(
                price_list_id=data.price_list_id,
                item_id=item_id,
                price=data.unit_price,
                description=data.service_type,
            )
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Price list item not found",
        ) from None


@router.delete(
    "/{item_id}",
)
async def delete(
    item_id: UUID,
    price_list_id: UUID,
    service: PriceListApplicationService = Depends(
        get_price_list_service,
    ),
):
    try:
        return await service.remove_item(
            RemovePriceListItemCommand(
                price_list_id=price_list_id,
                item_id=item_id,
            )
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Price list item not found",
        ) from None
