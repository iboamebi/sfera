from uuid import uuid4

from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.organization import (
    create_organization,
    router,
    update_organization,
)
from app.api.security.csrf import require_csrf
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


def get_route_dependencies(endpoint: object) -> list[object]:
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is endpoint
    )
    return [dependency.call for dependency in route.dependant.dependencies]


def test_create_organization_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(create_organization)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_create_organization_passes_authenticated_user_to_application_service() -> None:
    user = User(
        id=uuid4(),
        username="operator",
        password_hash="hash",
        role=UserRole.OPERATOR,
    )

    class FakeOrganizationService:
        def __init__(self) -> None:
            self.received_user: User | None = None

        def create(self, command: object, received_user: User) -> object:
            self.received_user = received_user
            return object()

    service = FakeOrganizationService()

    result = create_organization(
        data=OrganizationCreate(name="Test Organization"),
        user=user,
        service=service,
    )

    assert result is not None
    assert service.received_user is user


def test_update_organization_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(update_organization)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_update_organization_passes_authenticated_user_to_application_service() -> None:
    organization_id = uuid4()
    user = User(
        id=uuid4(),
        username="operator",
        password_hash="hash",
        role=UserRole.OPERATOR,
    )

    class FakeOrganizationService:
        def __init__(self) -> None:
            self.received_user: User | None = None

        def update(self, command: object, received_user: User) -> object:
            assert command.organization_id == organization_id
            self.received_user = received_user
            return object()

    service = FakeOrganizationService()

    result = update_organization(
        organization_id=organization_id,
        data=OrganizationUpdate(name="Updated Organization"),
        user=user,
        service=service,
    )

    assert result is not None
    assert service.received_user is user
