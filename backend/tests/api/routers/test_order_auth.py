from datetime import UTC, datetime
from uuid import uuid4

from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.order import (
    add_order_item,
    create_order,
    register_order,
    router,
    update_order,
)
from app.api.security.csrf import require_csrf
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.schemas.order import OrderRead, OrderUpdate


def get_route_dependencies(endpoint: object) -> list[object]:
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is endpoint
    )
    return [dependency.call for dependency in route.dependant.dependencies]


def test_create_order_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(create_order)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_add_order_item_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(add_order_item)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_update_order_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(update_order)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_register_order_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(register_order)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_register_order_passes_authenticated_user_to_application_service() -> None:
    order_id = uuid4()
    user = User(
        id=uuid4(),
        username="operator",
        password_hash="hash",
        role=UserRole.OPERATOR,
    )

    class FakeOrderService:
        def __init__(self) -> None:
            self.received_user: User | None = None

        def register(self, command: object, received_user: User) -> object:
            assert command.order_id == order_id
            self.received_user = received_user
            return object()

    class FakeOrderReadService:
        def get(self, requested_id: object) -> OrderRead:
            assert requested_id == order_id
            now = datetime.now(UTC)
            return OrderRead(
                id=order_id,
                number="1001",
                customer_id=uuid4(),
                customer_name="Test Customer",
                status="REGISTERED",
                received_at=now,
                created_at=now,
                updated_at=now,
                planned_issue_at=None,
                issued_at=None,
                comment=None,
                archived=False,
                items=[],
            )

    service = FakeOrderService()

    result = register_order(
        order_id=order_id,
        user=user,
        service=service,
        read_service=FakeOrderReadService(),
    )

    assert result is not None
    assert service.received_user is user


def test_update_order_passes_authenticated_user_to_application_service() -> None:
    order_id = uuid4()
    user = User(
        id=uuid4(),
        username="operator",
        password_hash="hash",
        role=UserRole.OPERATOR,
    )

    class FakeOrderService:
        def __init__(self) -> None:
            self.received_user: User | None = None

        def update(self, command: object, received_user: User) -> object:
            assert command.order_id == order_id
            self.received_user = received_user
            return object()

    service = FakeOrderService()

    result = update_order(
        order_id=order_id,
        data=OrderUpdate(
            planned_issue_at=None,
            comment="Updated order",
        ),
        user=user,
        service=service,
    )

    assert result is not None
    assert service.received_user is user
