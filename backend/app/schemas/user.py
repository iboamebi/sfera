"""User administration API schemas."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domains.user.value_objects.user_role import UserRole


class UserCreate(BaseModel):
    """Fields accepted when an administrator creates a user."""

    username: str = Field(min_length=1, max_length=100)
    full_name: str = Field(min_length=1, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    position: str | None = Field(default=None, max_length=255)
    role: UserRole

    @field_validator("username", "full_name")
    @classmethod
    def strip_required_fields(cls, value: str) -> str:
        """Reject whitespace-only account identifiers and names."""
        normalized = value.strip()
        if not normalized:
            raise ValueError("Field must not be blank")
        return normalized


class UserProfileUpdate(BaseModel):
    """Employee profile fields accepted from user administration."""

    full_name: str = Field(min_length=1, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    position: str | None = Field(default=None, max_length=255)

    @field_validator("full_name")
    @classmethod
    def strip_full_name(cls, value: str) -> str:
        """Require a non-empty employee name."""
        normalized = value.strip()
        if not normalized:
            raise ValueError("Full name must not be blank")
        return normalized


class UserActiveUpdate(BaseModel):
    """Account activation state accepted by user administration."""

    is_active: bool


class UserRoleUpdate(BaseModel):
    """Role assignment accepted by user administration."""

    role: UserRole


class UserRead(BaseModel):
    """Public account and employee profile returned to administrators."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    full_name: str | None
    phone: str | None
    position: str | None
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
