from app.api.base_router import BaseRouter
from app.crud.order_item import order_item_crud
from app.schemas.order_item import (
    OrderItemCreate,
    OrderItemRead,
    OrderItemUpdate,
)

router = BaseRouter(
    crud=order_item_crud,
    read_schema=OrderItemRead,
    create_schema=OrderItemCreate,
    update_schema=OrderItemUpdate,
    prefix="/order-items",
    tags=["Order Items"],
).router
