"""
Command: update organization.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateOrganizationCommand:
    """Update organization command."""

    organization_id: UUID
    name: str | None = None
    short_name: str | None = None
    inn: str | None = None
    kpp: str | None = None
    ogrn: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    comment: str | None = None
