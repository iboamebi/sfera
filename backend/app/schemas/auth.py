"""Authentication API schemas."""

from uuid import UUID

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Credentials submitted to the authentication endpoint."""

    username: str
    password: str


class AuthenticatedUserResponse(BaseModel):
    """Client-safe authenticated user representation."""

    id: UUID
    username: str
