from uuid import uuid4

from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.customer import (
    router,
    update_customer,
)
from app.api.security.csrf import require_csrf
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.schemas.customer import CustomerUpdate


def _route(path: str, method: str) -> APIRoute:
    for route in router.routes:
        if (
            isinstance(route, APIRoute)
            and route.path == path
            and method in route.methods
        ):
            return route
    raise AssertionError(f"Route not found: {method} {path}")


def _dependency_calls(route: APIRoute) -> set[object]:
    return {dependency.call for dependency in route.dependant.dependencies}


def test_customer_reads_do_not_require_authentication() -> None:
    assert get_current_user not in _dependency_calls(
        _route("/customers/", "GET"),
    )
    assert get_current_user not in _dependency_calls(
        _route("/customers/{customer_id}", "GET"),
    )


def test_customer_mutations_require_authentication_and_csrf() -> None:
    for method, path in (
        ("POST", "/customers/"),
        ("PATCH", "/customers/{customer_id}"),
        ("DELETE", "/customers/{customer_id}"),
    ):
        dependencies = _dependency_calls(_route(path, method))
        assert get_current_user in dependencies
        assert require_csrf in dependencies


def test_update_customer_passes_authenticated_user_to_application_service() -> None:
    customer_id = uuid4()
    user = User(
        id=uuid4(),
        username="operator",
        password_hash="hash",
        role=UserRole.OPERATOR,
    )

    class FakeCustomerService:
        def __init__(self) -> None:
            self.received_user: User | None = None

        def update(self, command: object, received_user: User) -> object:
            assert command.customer_id == customer_id
            self.received_user = received_user
            return object()

    service = FakeCustomerService()

    result = update_customer(
        customer_id=customer_id,
        data=CustomerUpdate(
            name="Updated Customer",
        ),
        user=user,
        service=service,
    )

    assert result is not None
    assert service.received_user is user
