"""
Domain entity: Organization.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class Organization:
    """
    Organization domain entity.
    """

    id: UUID
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
