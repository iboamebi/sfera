"""
Material domain entity.
"""

from dataclasses import dataclass

from app.shared.base.entity import Entity


@dataclass(eq=False)
class Material(Entity):
    """Material entity."""

    name: str
    article: str | None = None
    unit: str = ""
    description: str | None = None
    archived: bool = False
