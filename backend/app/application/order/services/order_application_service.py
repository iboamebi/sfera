"""
Application service for Order.
"""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.application.authorization.authorization import require_role
from app.application.context.operation_context import OperationContext
from app.application.order.commands.add_order_item import (
    AddOrderItemCommand,
)
from app.application.order.commands.create_order import (
    CreateOrderCommand,
)
from app.application.order.commands.register_order import (
    RegisterOrderCommand,
)
from app.application.order.commands.update_order import (
    UpdateOrderCommand,
)
from app.application.order.exceptions import (
    InstrumentAlreadyInActiveOrderApplicationError,
    OrderItemNotFoundApplicationError,
    OrderNotFoundApplicationError,
)
from app.domains.order.entities.order import Order
from app.domains.order.entities.order_item import OrderItem
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class OrderApplicationService:
    """Coordinates Order use cases."""

    def __init__(
        self,
        repository: OrderRepository,
        unit_of_work: UnitOfWork,
        event_dispatcher: object | None = None,
    ) -> None:
        self._repository = repository
        self._uow = unit_of_work
        self._event_dispatcher = event_dispatcher

    def create(
        self,
        command: CreateOrderCommand,
        user: User,
    ) -> Order:
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)

        with self._uow:
            order = Order.create(
                id=uuid4(),
                number=OrderNumber(command.number),
                customer_id=command.customer_id,
                received_at=datetime.now(UTC),
                planned_issue_at=command.planned_issue_at,
                comment=command.comment,
            )

            self._repository.save(order)

        return order

    def get(
        self,
        order_id: UUID,
    ) -> Order:
        """Get order."""

        order = self._repository.get(order_id)

        if order is None:
            raise OrderNotFoundApplicationError

        return order

    def list(
        self,
    ) -> list[Order]:
        """List orders."""

        return self._repository.list()

    def add_item(
        self,
        command: AddOrderItemCommand,
        user: User,
    ) -> Order:
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)

        with self._uow:
            order = self.get(command.order_id)

            if (
                command.instrument_id is not None
                and self._repository.has_conflicting_order_for_instrument(
                    command.instrument_id,
                    exclude_order_id=order.id,
                )
            ):
                raise InstrumentAlreadyInActiveOrderApplicationError

            order.add_item(
                OrderItem(
                    id=uuid4(),
                    instrument_id=command.instrument_id,
                    requested_operations=set(command.requested_operations),
                )
            )

            self._repository.save(order)

        return order

    def remove_item(
        self,
        order_id: UUID,
        item_id: UUID,
        user: User,
    ) -> None:
        """Remove an item from a new order."""

        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)

        with self._uow:
            order = self.get(order_id)

            if not order.remove_item(item_id):
                raise OrderItemNotFoundApplicationError

            if not self._repository.delete_item(order_id, item_id):
                raise OrderItemNotFoundApplicationError

    def update(
        self,
        command: UpdateOrderCommand,
        user: User,
    ) -> Order:
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)

        with self._uow:
            order = self.get(command.order_id)

            order.update_details(
                planned_issue_at=command.planned_issue_at,
                comment=command.comment,
            )

            self._repository.save(order)

        return order

    def register(
        self,
        command: RegisterOrderCommand,
        user: User,
    ) -> Order:
        require_role(user, UserRole.OPERATOR, UserRole.ADMIN)

        operation_context = OperationContext(
            operation_id=uuid4(),
            actor_id=user.id,
        )

        with self._uow:
            order = self.get(command.order_id)

            order.register()

            self._uow.register_aggregate(
                order,
                operation_context.operation_id,
            )

            self._repository.save(order)

        return order
