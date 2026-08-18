from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.diagnostic import (
    complete_diagnostic,
    create_diagnostic,
    router,
    set_recommendation,
)
from app.api.security.csrf import require_csrf


def get_route_dependencies(endpoint: object) -> list[object]:
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is endpoint
    )
    return [dependency.call for dependency in route.dependant.dependencies]


def test_create_diagnostic_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(create_diagnostic)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_complete_diagnostic_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(complete_diagnostic)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_set_recommendation_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(set_recommendation)

    assert get_current_user in dependencies
    assert require_csrf in dependencies
