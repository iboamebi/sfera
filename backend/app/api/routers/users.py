"""Administrator-only user management endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.user.commands.archive_user import ArchiveUserCommand
from app.application.user.commands.change_user_role import ChangeUserRoleCommand
from app.application.user.commands.create_user import CreateUserCommand
from app.application.user.commands.reset_user_password import ResetUserPasswordCommand
from app.application.user.commands.restore_user import RestoreUserCommand
from app.application.user.commands.set_user_active import SetUserActiveCommand
from app.application.user.exceptions import (
    LastActiveAdministratorApplicationError,
    UserAlreadyExistsApplicationError,
    UserNotFoundApplicationError,
)
from app.application.user.services.user_administration_application_service import (
    UserAdministrationApplicationService,
)
from app.core.dependencies.services import get_user_administration_service
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.schemas.user import (
    UserActiveUpdate,
    UserCreate,
    UserCreated,
    UserPasswordReset,
    UserRead,
    UserRoleUpdate,
)

router = APIRouter(
    prefix="/users",
    tags=["User Administration"],
)


@router.get(
    "/",
    response_model=list[UserRead],
)
def get_users(
    include_archived: bool = Query(default=False),
    user: User = Depends(get_current_user),
    service: UserAdministrationApplicationService = Depends(
        get_user_administration_service,
    ),
) -> list[User]:
    """List user accounts for administrators."""
    return service.get_all(user, include_archived=include_archived)


@router.patch(
    "/{user_id}/role",
    response_model=UserRead,
    dependencies=[Depends(require_csrf)],
)
def change_user_role(
    user_id: UUID,
    data: UserRoleUpdate,
    actor: User = Depends(get_current_user),
    service: UserAdministrationApplicationService = Depends(
        get_user_administration_service,
    ),
) -> User:
    """Change a user's role."""
    try:
        return service.change_role(
            ChangeUserRoleCommand(user_id=user_id, role=data.role),
            actor,
        )
    except LastActiveAdministratorApplicationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="At least one active administrator must remain",
        ) from None
    except UserNotFoundApplicationError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from None


@router.patch(
    "/{user_id}/status",
    response_model=UserRead,
    dependencies=[Depends(require_csrf)],
)
def set_user_active(
    user_id: UUID,
    data: UserActiveUpdate,
    actor: User = Depends(get_current_user),
    service: UserAdministrationApplicationService = Depends(
        get_user_administration_service,
    ),
) -> User:
    """Activate or deactivate a user account."""
    try:
        return service.set_active(
            SetUserActiveCommand(user_id=user_id, is_active=data.is_active),
            actor,
        )
    except LastActiveAdministratorApplicationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="At least one active administrator must remain",
        ) from None
    except UserNotFoundApplicationError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from None


@router.post(
    "/{user_id}/archive",
    response_model=UserRead,
    dependencies=[Depends(require_csrf)],
)
def archive_user(
    user_id: UUID,
    actor: User = Depends(get_current_user),
    service: UserAdministrationApplicationService = Depends(
        get_user_administration_service,
    ),
) -> User:
    """Archive a user account without deleting its history."""
    try:
        return service.archive(ArchiveUserCommand(user_id=user_id), actor)
    except LastActiveAdministratorApplicationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="At least one active administrator must remain",
        ) from None
    except UserNotFoundApplicationError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from None


@router.post(
    "/{user_id}/restore",
    response_model=UserRead,
    dependencies=[Depends(require_csrf)],
)
def restore_user(
    user_id: UUID,
    actor: User = Depends(get_current_user),
    service: UserAdministrationApplicationService = Depends(
        get_user_administration_service,
    ),
) -> User:
    """Restore an archived user account."""
    try:
        return service.restore(RestoreUserCommand(user_id=user_id), actor)
    except UserNotFoundApplicationError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from None


@router.post(
    "/{user_id}/reset-password",
    response_model=UserPasswordReset,
    dependencies=[Depends(require_csrf)],
)
def reset_user_password(
    user_id: UUID,
    actor: User = Depends(get_current_user),
    service: UserAdministrationApplicationService = Depends(
        get_user_administration_service,
    ),
) -> UserPasswordReset:
    """Reset a user's password and return its temporary value once."""
    try:
        user, temporary_password = service.reset_password(
            ResetUserPasswordCommand(user_id=user_id),
            actor,
        )
    except UserNotFoundApplicationError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from None

    return UserPasswordReset(
        id=user.id,
        username=user.username,
        role=user.role,
        is_active=user.is_active,
        archived=user.archived,
        must_change_password=user.must_change_password,
        temporary_password=temporary_password,
    )


@router.post(
    "/",
    response_model=UserCreated,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_csrf)],
)
def create_user(
    data: UserCreate,
    actor: User = Depends(get_current_user),
    service: UserAdministrationApplicationService = Depends(
        get_user_administration_service,
    ),
) -> UserCreated:
    """Create a user and return its temporary password once."""
    try:
        user, temporary_password = service.create(
            CreateUserCommand(
                username=data.username,
                role=UserRole(data.role),
            ),
            actor,
        )
    except UserAlreadyExistsApplicationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        ) from None

    return UserCreated(
        id=user.id,
        username=user.username,
        role=user.role,
        is_active=user.is_active,
        archived=user.archived,
        must_change_password=user.must_change_password,
        temporary_password=temporary_password,
    )
