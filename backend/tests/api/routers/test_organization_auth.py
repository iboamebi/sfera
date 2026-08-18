from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.organization import create_organization, router, update_organization
from app.api.security.csrf import require_csrf


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


def test_update_organization_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(update_organization)

    assert get_current_user in dependencies
    assert require_csrf in dependencies
