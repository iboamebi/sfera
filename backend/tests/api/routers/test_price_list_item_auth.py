from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.price_list_item import create, delete, router, update
from app.api.security.csrf import require_csrf


def get_route_dependencies(endpoint: object) -> list[object]:
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is endpoint
    )
    return [dependency.call for dependency in route.dependant.dependencies]


def test_create_price_list_item_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(create)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_update_price_list_item_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(update)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_delete_price_list_item_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(delete)

    assert get_current_user in dependencies
    assert require_csrf in dependencies
