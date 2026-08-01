"""
Organization API schemas.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class OrganizationBase(BaseModel):
    """Organization base schema."""

    name: str
    short_name: str | None = None
    inn: str | None = None
    kpp: str | None = None
    ogrn: str | None = None
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    website: str | None = None
    comment: str | None = None


class OrganizationCreate(OrganizationBase):
    """Organization create schema."""


class OrganizationUpdate(BaseModel):
    """Organization update schema."""

    name: str | None = None
    short_name: str | None = None
    inn: str | None = None
    kpp: str | None = None
    ogrn: str | None = None
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    website: str | None = None
    comment: str | None = None


class OrganizationRead(OrganizationBase):
    """Organization read schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
