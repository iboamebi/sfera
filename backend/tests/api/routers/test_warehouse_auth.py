from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.warehouse import create_warehouse, router as warehouse_router
from app.api.routers.warehouse_movement import (
    create_movement,
    router as movement_router,
)
from app.api.routers.warehouse_stock import add_stock, router as stock_router
from app.api.security.csrf import require_csrf


def get_route_dependencies(router, endpoint):
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is endpoint
    )
    return [dependency.call for dependency in route.dependant.dependencies]


def assert_write_route_is_protected(router, endpoint):
    dependencies = get_route_dependencies(router, endpoint)
    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_create_warehouse_requires_authentication_and_csrf() -> None:
    assert_write_route_is_protected(warehouse_router, create_warehouse)


def test_add_stock_requires_authentication_and_csrf() -> None:
    assert_write_route_is_protected(stock_router, add_stock)


def test_create_movement_requires_authentication_and_csrf() -> None:
    assert_write_route_is_protected(movement_router, create_movement)
