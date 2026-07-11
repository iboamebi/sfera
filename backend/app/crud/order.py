from app.crud.base import BaseCRUD
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate


class OrderCRUD(
    BaseCRUD[
        Order,
        OrderCreate,
        OrderUpdate,
    ]
):
    pass


order_crud = OrderCRUD(Order)
