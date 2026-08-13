"""
Order API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.order.commands.add_order_item import (
    AddOrderItemCommand,
)
from app.application.order.commands.create_order import (
    CreateOrderCommand,
)
from app.application.order.commands.register_order import (
    RegisterOrderCommand,
)
from app.application.order.exceptions import (
    OrderNotFoundApplicationError,
)
from app.application.order.services.order_application_service import (
    OrderApplicationService,
)
from app.core.dependencies.services import get_order_service
from app.schemas.order import (
    OrderCreate,
    OrderRead,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


class OrderItemCreate(BaseModel):
    """Request schema for adding an order item."""

    instrument_id: UUID | None = None


@router.post(
    "/",
    response_model=OrderRead,
    status_code=201,
)
def create_order(
    data: OrderCreate,
    service: OrderApplicationService = Depends(
        get_order_service,
    ),
):
    return service.create(
        CreateOrderCommand(
            customer_id=data.customer_id,
            number=data.number,
        )
    )


@router.get(
    "/",
    response_model=list[OrderRead],
)
def list_orders(
    service: OrderApplicationService = Depends(
        get_order_service,
    ),
):
    return service.list()


@router.post(
    "/{order_id}/items",
    response_model=OrderRead,
)
def add_order_item(
    order_id: UUID,
    data: OrderItemCreate,
    service: OrderApplicationService = Depends(
        get_order_service,
    ),
):
    return service.add_item(
        AddOrderItemCommand(
            order_id=order_id,
            instrument_id=data.instrument_id,
        )
    )


@router.post(
    "/{order_id}/register",
    response_model=OrderRead,
)
def register_order(
    order_id: UUID,
    service: OrderApplicationService = Depends(
        get_order_service,
    ),
):
    return service.register(
        RegisterOrderCommand(
            order_id=order_id,
        )
    )


@router.get(
    "/{order_id}",
    response_model=OrderRead,
)
def get_order(
    order_id: UUID,
    service: OrderApplicationService = Depends(
        get_order_service,
    ),
):
    try:
        return service.get(order_id)

    except OrderNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        ) from None
