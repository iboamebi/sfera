"""
Site API schemas.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SiteCreate(BaseModel):
    """Site create schema."""

    organization_id: UUID
    name: str
    address: str


class SiteRead(BaseModel):
    """Site read schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    name: str
    address: str
    archived: bool
