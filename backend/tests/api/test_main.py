from fastapi import Request

from app.application.authorization.authorization import AuthorizationError
from app.main import authorization_error_handler


def test_authorization_error_maps_to_forbidden_response() -> None:
    response = authorization_error_handler(
        Request({"type": "http", "method": "POST", "path": "/orders/1/register"}),
        AuthorizationError("User is not authorized for this action"),
    )

    assert response.status_code == 403
    assert response.body == b'{"detail":"User is not authorized for this action"}'
