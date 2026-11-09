from fastapi import Request
from fastapi.routing import APIRoute

from app.api.dependencies.auth import require_password_change_completed
from app.application.authorization.authorization import AuthorizationError
from app.main import app, authorization_error_handler


def test_authorization_error_maps_to_forbidden_response() -> None:
    response = authorization_error_handler(
        Request({"type": "http", "method": "POST", "path": "/orders/1/register"}),
        AuthorizationError("User is not authorized for this action"),
    )

    assert response.status_code == 403
    assert response.body == b'{"detail":"User is not authorized for this action"}'


def test_all_business_routers_require_first_login_password_completion() -> None:
    included_routers = [
        route.include_context
        for route in app.routes
        if getattr(route, "include_context", None) is not None
    ]
    business_routers = [
        context
        for context in included_routers
        if context.included_router.prefix != "/auth"
    ]

    assert business_routers
    for context in business_routers:
        assert any(
            dependency.dependency is require_password_change_completed
            for dependency in context.dependencies
        ), context.included_router.prefix


def test_authentication_and_health_routes_are_not_gated() -> None:
    auth_routers = [
        route.include_context
        for route in app.routes
        if getattr(route, "include_context", None) is not None
        and route.include_context.included_router.prefix == "/auth"
    ]
    health_routes = [
        route
        for route in app.routes
        if isinstance(route, APIRoute) and route.path == "/health"
    ]

    assert auth_routers
    assert health_routes
    for context in auth_routers:
        assert all(
            dependency.dependency is not require_password_change_completed
            for dependency in context.dependencies
        )
    for route in health_routes:
        assert all(
            dependency.call is not require_password_change_completed
            for dependency in route.dependant.dependencies
        ), route.path
