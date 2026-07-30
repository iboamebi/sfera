"""
Warehouse domain entity.
"""

from dataclasses import dataclass

from app.shared.base.entity import Entity


@dataclass(eq=False)
class Warehouse(Entity):
    """Warehouse entity."""

    name: str
    address: str | None = None
    responsible_person: str | None = None
    comment: str | None = None
    archived: bool = False
