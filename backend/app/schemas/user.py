"""User administration API schemas."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domains.user.value_objects.user_role import UserRole


class UserCreate(BaseModel):
    """Fields accepted when an administrator creates a user."""

    username: str = Field(min_length=1, max_length=100)
    role: UserRole


class UserActiveUpdate(BaseModel):
    """Account activation state accepted by user administration."""

    is_active: bool


class UserRoleUpdate(BaseModel):
    """Role assignment accepted by user administration."""

    role: UserRole


class UserRead(BaseModel):
    """Public account state returned to administrators."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    role: UserRole
    is_active: bool
    archived: bool
    must_change_password: bool


class UserCreated(UserRead):
    """New account response containing its one-time temporary password."""

    temporary_password: str


class UserPasswordReset(UserRead):
    """Account state and one-time temporary password returned after reset."""

    temporary_password: str
