"""
Domain entity: Organization.
"""

from dataclasses import dataclass

from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class Organization(Entity):
    """
    Organization domain entity.
    """

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
