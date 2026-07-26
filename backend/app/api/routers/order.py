"""
Order API router.
"""

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.application.order.services.order_service import OrderService
from app.core.dependencies.services import get_order_service
from app.schemas.order import (
    OrderCreate,
    OrderRead,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "/",
    response_model=OrderRead,
    status_code=201,
)
def create_order(
    data: OrderCreate,
    service: OrderService = Depends(
        get_order_service,
    ),
):
    try:
        return service.create(
            order_id=uuid4(),
            customer_id=data.customer_id,
            number=data.number,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "/{order_id}",
    response_model=OrderRead,
)
def get_order(
    order_id: UUID,
    service: OrderService = Depends(
        get_order_service,
    ),
):
    try:
        return service.get(order_id)

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        ) from None
