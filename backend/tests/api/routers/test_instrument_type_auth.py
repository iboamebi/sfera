from fastapi.routing import APIRoute

from app.api.dependencies.auth import get_current_user
from app.api.routers.instrument_type import (
    archive_instrument_type,
    create_instrument_type,
    restore_instrument_type,
    router,
    update_instrument_type,
)
from app.api.security.csrf import require_csrf


def get_route_dependencies(endpoint: object) -> list[object]:
    route = next(
        route
        for route in router.routes
        if isinstance(route, APIRoute) and route.endpoint is endpoint
    )
    return [dependency.call for dependency in route.dependant.dependencies]


def test_create_instrument_type_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(create_instrument_type)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_update_instrument_type_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(update_instrument_type)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_archive_instrument_type_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(archive_instrument_type)

    assert get_current_user in dependencies
    assert require_csrf in dependencies


def test_restore_instrument_type_requires_authentication_and_csrf() -> None:
    dependencies = get_route_dependencies(restore_instrument_type)

    assert get_current_user in dependencies
    assert require_csrf in dependencies
