from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.repair import (
    cancel_repair,
    complete_repair,
    create_repair,
    router,
    start_repair,
)
from app.api.security.csrf import require_csrf


def get_route_dependencies(endpoint: object) -> list[object]:
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is endpoint
    )
    return [dependency.call for dependency in route.dependant.dependencies]


def test_create_repair_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(create_repair)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_start_repair_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(start_repair)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_complete_repair_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(complete_repair)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_cancel_repair_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(cancel_repair)

    assert get_current_user in dependencies
    assert require_csrf in dependencies
