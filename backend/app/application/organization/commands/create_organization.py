"""
Command: create organization.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateOrganizationCommand:
    """Create organization command."""

    name: str
    short_name: str | None = None
    inn: str | None = None
    kpp: str | None = None
    ogrn: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    comment: str | None = None
