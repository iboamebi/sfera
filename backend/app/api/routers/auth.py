"""Authentication API endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status

from app.api.security.csrf import generate_csrf_token, require_csrf
from app.application.auth.commands.authenticate_user import AuthenticateUserCommand
from app.application.auth.commands.create_session import CreateSessionCommand
from app.application.auth.commands.get_current_user import GetCurrentUserCommand
from app.application.auth.commands.revoke_session import RevokeSessionCommand
from app.application.auth.exceptions import AuthenticationFailedApplicationError
from app.application.auth.services.authentication_application_service import (
    AuthenticationApplicationService,
)
from app.application.auth.services.current_user_application_service import (
    CurrentUserApplicationService,
)
from app.application.auth.services.session_application_service import (
    SessionApplicationService,
)
from app.core.config import settings
from app.core.dependencies.services import (
    get_authentication_service,
    get_current_user_service,
    get_session_service,
)
from app.core.dependencies.uow import get_unit_of_work
from app.schemas.auth import AuthenticatedUserResponse, LoginRequest
from app.shared.unit_of_work.unit_of_work import UnitOfWork

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=AuthenticatedUserResponse,
)
def login(
    data: LoginRequest,
    response: Response,
    authentication_service: AuthenticationApplicationService = Depends(
        get_authentication_service,
    ),
    session_service: SessionApplicationService = Depends(get_session_service),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> AuthenticatedUserResponse:
    """Authenticate user and establish a server-side session."""

    try:
        user = authentication_service.authenticate(
            AuthenticateUserCommand(
                username=data.username,
                password=data.password,
            ),
        )
    except AuthenticationFailedApplicationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        ) from None

    session = session_service.create(
        CreateSessionCommand(
            user_id=user.id,
            now=datetime.now(UTC),
        ),
    )
    uow.commit()

    response.set_cookie(
        key=settings.AUTH_COOKIE_NAME,
        value=session.session_id,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        max_age=settings.AUTH_SESSION_TTL_SECONDS,
    )
    response.set_cookie(
        key=settings.CSRF_COOKIE_NAME,
        value=generate_csrf_token(),
        httponly=False,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        max_age=settings.AUTH_SESSION_TTL_SECONDS,
    )

    return AuthenticatedUserResponse(
        id=user.id,
        username=user.username,
    )


@router.get(
    "/me",
    response_model=AuthenticatedUserResponse,
)
def get_current_user(
    session_id: str | None = Cookie(default=None, alias=settings.AUTH_COOKIE_NAME),
    service: CurrentUserApplicationService = Depends(get_current_user_service),
) -> AuthenticatedUserResponse:
    """Return the current authenticated user."""

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

    return AuthenticatedUserResponse(
        id=user.id,
        username=user.username,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    request: Request,
    response: Response,
    session_id: str | None = Cookie(default=None, alias=settings.AUTH_COOKIE_NAME),
    session_service: SessionApplicationService = Depends(get_session_service),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> None:
    """Revoke the current authenticated session and clear its cookies."""

    if session_id is not None:
        require_csrf(request)
        session_service.revoke(
            RevokeSessionCommand(
                session_id=session_id,
            ),
        )
        uow.commit()

    response.delete_cookie(
        key=settings.AUTH_COOKIE_NAME,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=True,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )
    response.delete_cookie(
        key=settings.CSRF_COOKIE_NAME,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=False,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )
