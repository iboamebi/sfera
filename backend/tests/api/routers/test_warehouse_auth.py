from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.warehouse import create_warehouse, router
from app.api.security.csrf import require_csrf


def test_create_warehouse_requires_authentication_and_csrf() -> None:
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is create_warehouse
    )
    dependencies = [dependency.call for dependency in route.dependant.dependencies]

    assert get_current_user in dependencies
    assert require_csrf in dependencies
