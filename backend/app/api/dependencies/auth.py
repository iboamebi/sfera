"""Authentication dependencies for protected API endpoints."""

from datetime import UTC, datetime

from fastapi import Cookie, Depends, HTTPException, Request, status

from app.application.auth.commands.get_current_user import GetCurrentUserCommand
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.application.auth.services.current_user_application_service import (
    CurrentUserApplicationService,
)
from app.core.config import settings
from app.core.dependencies.services import get_current_user_service
from app.domains.user.entities.user import User

_PASSWORD_CHANGE_EXEMPT_PATHS = {
    "/auth/login",
    "/auth/me",
    "/auth/logout",
    "/auth/change-password",
    "/health",
    "/openapi.json",
    "/docs",
    "/docs/oauth2-redirect",
    "/redoc",
}


def get_current_user(
    session_id: str | None = Cookie(default=None, alias=settings.AUTH_COOKIE_NAME),
    service: CurrentUserApplicationService = Depends(get_current_user_service),
) -> User:
    """Return the authenticated user or raise HTTP 401."""

    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        return service.get(
            GetCurrentUserCommand(
                session_id=session_id,
                now=datetime.now(UTC),
            ),
        )
    except AuthenticationFailedApplicationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        ) from None


def require_password_change_completed(
    request: Request,
    service: CurrentUserApplicationService = Depends(get_current_user_service),
) -> None:
    """Require authentication and a completed first-login password change."""

    if request.url.path in _PASSWORD_CHANGE_EXEMPT_PATHS:
        return

    session_id = request.cookies.get(settings.AUTH_COOKIE_NAME)
    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        user = service.get(
            GetCurrentUserCommand(
                session_id=session_id,
                now=datetime.now(UTC),
            ),
        )
    except AuthenticationFailedApplicationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        ) from None

    if user.must_change_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password change required",
        )
