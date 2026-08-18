"""Authentication dependencies for protected API endpoints."""

from datetime import UTC, datetime

from fastapi import Cookie, Depends, HTTPException, status

from app.application.auth.commands.get_current_user import GetCurrentUserCommand
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.application.auth.services.current_user_application_service import (
    CurrentUserApplicationService,
)
from app.core.config import settings
from app.core.dependencies.services import get_current_user_service
from app.domains.user.entities.user import User


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
