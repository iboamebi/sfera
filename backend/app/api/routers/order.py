from app.api.base_router import BaseRouter
from app.crud.order import order_crud
from app.schemas.order import (
    OrderCreate,
    OrderRead,
    OrderUpdate,
)

router = BaseRouter(
    crud=order_crud,
    read_schema=OrderRead,
    create_schema=OrderCreate,
    update_schema=OrderUpdate,
    prefix="/orders",
    tags=["Orders"],
).router
