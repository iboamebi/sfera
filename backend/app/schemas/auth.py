"""Authentication API schemas."""

from uuid import UUID

from pydantic import BaseModel

from app.domains.user.value_objects.user_role import UserRole


class LoginRequest(BaseModel):
    """Credentials submitted to the authentication endpoint."""

    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    """Current and replacement password submitted by an authenticated user."""

    current_password: str
    new_password: str


class AuthenticatedUserResponse(BaseModel):
    """Client-safe authenticated user representation."""

    id: UUID
    username: str
    role: UserRole
    must_change_password: bool
