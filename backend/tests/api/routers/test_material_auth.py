from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.material import archive_material, create_material, router, update_material
from app.api.security.csrf import require_csrf


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
