from uuid import uuid4

from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.material import (
    archive_material,
    create_material,
    router,
    update_material,
)
from app.api.security.csrf import require_csrf
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.schemas.material import MaterialUpdate


def get_route_dependencies(endpoint: object) -> list[object]:
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is endpoint
    )
    return [dependency.call for dependency in route.dependant.dependencies]


def test_create_material_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(create_material)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_update_material_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(update_material)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_archive_material_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(archive_material)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_update_material_passes_authenticated_user_to_application_service() -> None:
    material_id = uuid4()
    user = User(
        id=uuid4(),
        username="warehouse",
        password_hash="hash",
        role=UserRole.WAREHOUSE,
    )

    class FakeMaterialService:
        def __init__(self) -> None:
            self.received_user: User | None = None

        def update(self, command: object, received_user: User) -> object:
            assert command.material_id == material_id
            assert command.name == "Updated Material"
            self.received_user = received_user
            return object()

    service = FakeMaterialService()

    result = update_material(
        material_id=material_id,
        data=MaterialUpdate(name="Updated Material"),
        user=user,
        service=service,
    )

    assert result is not None
    assert service.received_user is user
