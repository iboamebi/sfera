"""Domain entity: Site."""

from dataclasses import dataclass
from uuid import UUID

from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class Site(Entity):
    """Customer site domain entity."""

    customer_id: UUID
    name: str
    address: str
    archived: bool = False
