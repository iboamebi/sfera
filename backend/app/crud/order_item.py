from app.crud.base import BaseCRUD
from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate


class OrderItemCRUD(
    BaseCRUD[
        OrderItem,
        OrderItemCreate,
        OrderItemUpdate,
    ]
):
    pass


order_item_crud = OrderItemCRUD(OrderItem)
