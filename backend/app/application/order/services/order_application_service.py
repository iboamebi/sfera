"""
Application service for Order use cases.
"""

from uuid import UUID, uuid4

from app.application.order.commands.add_order_item import AddOrderItemCommand
from app.application.order.commands.add_order_items import AddOrderItemsCommand
from app.application.order.commands.create_order import CreateOrderCommand
from app.application.order.commands.update_order import UpdateOrderCommand
from app.application.order.exceptions import (
    InstrumentAlreadyInActiveOrderApplicationError,
    OrderItemNotFoundApplicationError,
    OrderNotFoundApplicationError,
)
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.entities.order import Order
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.order.value_objects.order_status import OrderStatus
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.auth.permissions import require_role
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class OrderApplicationService:
    """Coordinates Order use cases."""

    def __init__(self, repository: OrderRepository, unit_of_work: UnitOfWork) -> None:
        self._repository = repository
        self._uow = unit_of_work

    def get(self, order_id: UUID) -> Order:
        """Get order by identifier."""
        order = self._repository.get(order_id)
        if order is None:
            raise OrderNotFoundApplicationError
        return order

    def list(self) -> list[Order]:
        """List orders."""
        return self._repository.list()

    def create(self, command: CreateOrderCommand, user: User) -> Order:
        """Create order."""
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)
        with self._uow:
            order = Order.create(id=uuid4(), number=command.number, customer_id=command.customer_id, received_at=command.received_at, planned_issue_at=command.planned_issue_at, comment=command.comment)
            self._repository.save(order)
        return order

    def add_item(self, command: AddOrderItemCommand, user: User) -> Order:
        """Add one item to an order."""
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)
        with self._uow:
            order = self.get(command.order_id)
            if command.instrument_id is not None and self._repository.has_conflicting_order_for_instrument(command.instrument_id, exclude_order_id=order.id):
                raise InstrumentAlreadyInActiveOrderApplicationError
            order.add_item(OrderItem(id=uuid4(), instrument_id=command.instrument_id, instrument_type_id=command.instrument_type_id, requested_operations=set(command.requested_operations)))
            self._repository.save(order)
        return order

    def add_items(self, command: AddOrderItemsCommand, user: User) -> Order:
        """Add multiple type-only items in one transaction."""
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)
        if command.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        with self._uow:
            order = self.get(command.order_id)
            for _ in range(command.quantity):
                order.add_item(OrderItem(id=uuid4(), instrument_type_id=command.instrument_type_id, requested_operations=set(command.requested_operations)))
            self._repository.save(order)
        return order

    def assign_item_instrument(self, order_id: UUID, item_id: UUID, instrument_id: UUID, user: User) -> Order:
        """Assign a concrete instrument to an order item."""
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)
        with self._uow:
            order = self.get(order_id)
            if self._repository.has_conflicting_order_for_instrument(instrument_id, exclude_order_id=order.id):
                raise InstrumentAlreadyInActiveOrderApplicationError
            if not any(item.id == item_id for item in order.items):
                raise OrderItemNotFoundApplicationError
            order.assign_instrument(item_id, instrument_id)
            self._repository.save(order)
        return order

    def remove_item(self, order_id: UUID, item_id: UUID, user: User) -> None:
        """Remove an item from a new order."""
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)
        with self._uow:
            order = self.get(order_id)
            if not order.remove_item(item_id):
                raise OrderItemNotFoundApplicationError
            self._repository.delete_item(order_id, item_id)

    def update(self, command: UpdateOrderCommand, user: User) -> Order:
        """Update editable order details."""
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)
        with self._uow:
            order = self.get(command.order_id)
            order.update_details(planned_issue_at=command.planned_issue_at, comment=command.comment)
            self._repository.save(order)
        return order
