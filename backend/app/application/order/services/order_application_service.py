"""
Application service for Order.
"""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.application.authorization.authorization import require_role
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
    ) -> None:
        self._repository = repository
        self._uow = unit_of_work

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

            order.add_item(
                OrderItem(
                    id=uuid4(),
                    instrument_id=command.instrument_id,
                )
            )

            self._repository.save(order)

        return order

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

        with self._uow:
            order = self.get(command.order_id)

            order.register()

            self._uow.register_aggregate(order)

            self._repository.save(order)

        return order
