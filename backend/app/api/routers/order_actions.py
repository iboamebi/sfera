"""
Order business actions.
"""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.order.services.order_service import OrderService
from app.core.dependencies.services import get_order_service

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/{order_id}/items")
def add_order_item(
    order_id: UUID,
    item_id: UUID,
    instrument_id: UUID | None = None,
    service: OrderService = Depends(get_order_service),
):
    return service.add_item(
        order_id,
        item_id,
        instrument_id,
    )


@router.post("/{order_id}/register")
def register_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service),
):
    return service.register(order_id)
