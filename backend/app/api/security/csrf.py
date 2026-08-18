"""CSRF protection helpers for cookie-authenticated requests."""

import secrets

from fastapi import HTTPException, Request, status

from app.core.config import settings


def generate_csrf_token() -> str:
    """Generate a cryptographically secure CSRF token."""

    return secrets.token_urlsafe(32)


def require_csrf(request: Request) -> None:
    """Require a valid double-submit CSRF token."""

    cookie_token = request.cookies.get(settings.CSRF_COOKIE_NAME)
    header_token = request.headers.get(settings.CSRF_HEADER_NAME)

    if not cookie_token or not header_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF validation failed",
        )

    if not secrets.compare_digest(cookie_token, header_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF validation failed",
        )
