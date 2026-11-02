"""Administrator-only user management endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.user.commands.change_user_role import ChangeUserRoleCommand
from app.application.user.commands.create_user import CreateUserCommand
from app.application.user.exceptions import (
    UserAlreadyExistsApplicationError,
    UserNotFoundApplicationError,
)
from app.application.user.services.user_administration_application_service import (
    UserAdministrationApplicationService,
)
from app.core.dependencies.services import get_user_administration_service
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.schemas.user import UserCreate, UserCreated, UserRead, UserRoleUpdate

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
    except UserNotFoundApplicationError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from None


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
