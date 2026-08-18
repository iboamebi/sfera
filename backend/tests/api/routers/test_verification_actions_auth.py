from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.verification_actions import (
    approve_verification,
    reject_verification,
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


def test_approve_verification_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(approve_verification)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_reject_verification_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(reject_verification)

    assert get_current_user in dependencies
    assert require_csrf in dependencies
