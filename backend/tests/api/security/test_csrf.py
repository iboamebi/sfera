from fastapi import HTTPException
from starlette.requests import Request

from app.api.security.csrf import generate_csrf_token, require_csrf
from app.core.config import settings


def make_request(
    cookie_token: str | None,
    header_token: str | None,
) -> Request:
    headers = []
    if header_token is not None:
        headers.append((settings.CSRF_HEADER_NAME.lower().encode(), header_token.encode()))

    cookie = ""
    if cookie_token is not None:
        cookie = f"{settings.CSRF_COOKIE_NAME}={cookie_token}"
        headers.append((b"cookie", cookie.encode()))

    scope = {
        "type": "http",
        "method": "POST",
        "path": "/auth/logout",
        "headers": headers,
        "query_string": b"",
        "server": ("testserver", 80),
        "client": ("testclient", 50000),
        "scheme": "http",
    }
    return Request(scope)


def test_generate_csrf_token_returns_random_url_safe_value() -> None:
    first = generate_csrf_token()
    second = generate_csrf_token()

    assert first != second
    assert len(first) >= 40
    assert all(character.isalnum() or character in "-_" for character in first)


def test_require_csrf_rejects_missing_tokens() -> None:
    request = make_request(None, None)

    try:
        require_csrf(request)
    except HTTPException as exc:
        assert exc.status_code == 403
        return

    raise AssertionError("Expected CSRF validation to fail")


def test_require_csrf_rejects_mismatched_tokens() -> None:
    request = make_request("cookie-token", "header-token")

    try:
        require_csrf(request)
    except HTTPException as exc:
        assert exc.status_code == 403
        return

    raise AssertionError("Expected CSRF validation to fail")


def test_require_csrf_accepts_matching_tokens() -> None:
    request = make_request("same-token", "same-token")

    require_csrf(request)
