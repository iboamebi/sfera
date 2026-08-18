from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.device import (
    connect_device,
    create_device,
    disconnect_device,
    router,
)
from app.api.security.csrf import require_csrf


def get_route_dependencies(endpoint: object) -> list[object]:
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is endpoint
    )
    return [dependency.call for dependency in route.dependant.dependencies]


def test_create_device_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(create_device)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_connect_device_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(connect_device)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_disconnect_device_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(disconnect_device)

    assert get_current_user in dependencies
    assert require_csrf in dependencies
