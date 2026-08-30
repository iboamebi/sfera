"""
Order API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.order.commands.add_order_item import AddOrderItemCommand
from app.application.order.commands.add_order_items import AddOrderItemsCommand
from app.application.order.commands.create_order import CreateOrderCommand
from app.application.order.commands.register_order import RegisterOrderCommand
from app.application.order.commands.update_order import UpdateOrderCommand
from app.application.order.exceptions import (
    InstrumentAlreadyInActiveOrderApplicationError,
    OrderItemNotFoundApplicationError,
    OrderNotFoundApplicationError,
)
from app.application.order.queries.order_read_service import OrderReadService
from app.application.order.services.order_application_service import OrderApplicationService
from app.core.dependencies.services import get_order_read_service, get_order_service
from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.domains.user.entities.user import User
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


class OrderItemCreate(BaseModel):
    """Request schema for adding an order item."""

    instrument_id: UUID | None = None
    instrument_type_id: UUID | None = None
    requested_operations: set[OrderItemOperation] = Field(default_factory=set)


class OrderItemsBulkCreate(BaseModel):
    """Request schema for mass intake of type-only order items."""

    instrument_type_id: UUID
    quantity: int = Field(gt=0)
    requested_operations: set[OrderItemOperation] = Field(default_factory=set)


class OrderItemInstrumentUpdate(BaseModel):
    """Request schema for assigning a concrete instrument to an order item."""

    instrument_id: UUID


@router.post(
    "/",
    response_model=OrderRead,
    status_code=201,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def create_order(
    data: OrderCreate,
    user: User = Depends(get_current_user),
    service: OrderApplicationService = Depends(get_order_service),
):
    return service.create(
        CreateOrderCommand(
            customer_id=data.customer_id,
            number=data.number,
            planned_issue_at=data.planned_issue_at,
            comment=data.comment,
        ),
        user,
    )


@router.get("/", response_model=list[OrderRead])
def list_orders(service: OrderApplicationService = Depends(get_order_service)):
    return service.list()


@router.post(
    "/{order_id}/items",
    response_model=OrderRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def add_order_item(
    order_id: UUID,
    data: OrderItemCreate,
    user: User = Depends(get_current_user),
    service: OrderApplicationService = Depends(get_order_service),
):
    try:
        return service.add_item(
            AddOrderItemCommand(
                order_id=order_id,
                instrument_id=data.instrument_id,
                instrument_type_id=data.instrument_type_id,
                requested_operations=frozenset(data.requested_operations),
            ),
            user,
        )
    except InstrumentAlreadyInActiveOrderApplicationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Instrument is already in another active order",
        ) from None


@router.post(
    "/{order_id}/items/bulk",
    response_model=OrderRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def add_order_items_bulk(
    order_id: UUID,
    data: OrderItemsBulkCreate,
    user: User = Depends(get_current_user),
    service: OrderApplicationService = Depends(get_order_service),
):
    try:
        return service.add_items(
            AddOrderItemsCommand(
                order_id=order_id,
                instrument_type_id=data.instrument_type_id,
                quantity=data.quantity,
                requested_operations=frozenset(data.requested_operations),
            ),
            user,
        )
    except OrderNotFoundApplicationError:
        raise HTTPException(status_code=404, detail="Order not found") from None


@router.patch(
    "/{order_id}/items/{item_id}/instrument",
    response_model=OrderRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def assign_order_item_instrument(
    order_id: UUID,
    item_id: UUID,
    data: OrderItemInstrumentUpdate,
    user: User = Depends(get_current_user),
    service: OrderApplicationService = Depends(get_order_service),
):
    try:
        return service.assign_item_instrument(order_id, item_id, data.instrument_id, user)
    except OrderNotFoundApplicationError:
        raise HTTPException(status_code=404, detail="Order not found") from None
    except OrderItemNotFoundApplicationError:
        raise HTTPException(status_code=404, detail="Order item not found") from None
    except InstrumentAlreadyInActiveOrderApplicationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Instrument is already in another active order",
        ) from None


@router.delete(
    "/{order_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def delete_order_item(
    order_id: UUID,
    item_id: UUID,
    user: User = Depends(get_current_user),
    service: OrderApplicationService = Depends(get_order_service),
) -> None:
    try:
        service.remove_item(order_id, item_id, user)
    except OrderNotFoundApplicationError:
        raise HTTPException(status_code=404, detail="Order not found") from None
    except OrderItemNotFoundApplicationError:
        raise HTTPException(status_code=404, detail="Order item not found") from None


@router.patch(
    "/{order_id}",
    response_model=OrderRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def update_order(
    order_id: UUID,
    data: OrderUpdate,
    user: User = Depends(get_current_user),
    service: OrderApplicationService = Depends(get_order_service),
):
    try:
        return service.update(
            UpdateOrderCommand(
                order_id=order_id,
                planned_issue_at=data.planned_issue_at,
                comment=data.comment,
            ),
            user,
        )
    except OrderNotFoundApplicationError:
        raise HTTPException(status_code=404, detail="Order not found") from None


@router.post(
    "/{order_id}/register",
    response_model=OrderRead,
    dependencies=[Depends(require_csrf)],
)
def register_order(
    order_id: UUID,
    user: User = Depends(get_current_user),
    service: OrderApplicationService = Depends(get_order_service),
):
    return service.register(RegisterOrderCommand(order_id=order_id), user)


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: UUID,
    service: OrderReadService = Depends(get_order_read_service),
):
    return service.get(order_id)
