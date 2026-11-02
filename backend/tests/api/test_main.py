from fastapi import Request
from fastapi.routing import APIRoute

from app.application.authorization.authorization import AuthorizationError
from app.api.dependencies.auth import require_password_change_completed
from app.main import app, authorization_error_handler


def test_authorization_error_maps_to_forbidden_response() -> None:
    response = authorization_error_handler(
        Request({"type": "http", "method": "POST", "path": "/orders/1/register"}),
        AuthorizationError("User is not authorized for this action"),
    )

    assert response.status_code == 403
    assert response.body == b'{"detail":"User is not authorized for this action"}'



def test_all_business_routes_require_first_login_password_completion() -> None:
    business_routes = [
        route
        for route in app.routes
        if isinstance(route, APIRoute)
        and not route.path.startswith("/auth/")
        and route.path != "/health"
    ]

    assert business_routes
    for route in business_routes:
        assert any(
            dependency.call is require_password_change_completed
            for dependency in route.dependant.dependencies
        ), route.path


def test_authentication_and_health_routes_are_not_gated() -> None:
    exempt_routes = [
        route
        for route in app.routes
        if isinstance(route, APIRoute)
        and (route.path.startswith("/auth/") or route.path == "/health")
    ]

    assert exempt_routes
    for route in exempt_routes:
        assert all(
            dependency.call is not require_password_change_completed
            for dependency in route.dependant.dependencies
        ), route.path
