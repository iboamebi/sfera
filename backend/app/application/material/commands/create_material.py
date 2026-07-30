"""
Create Material command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateMaterialCommand:
    """Create material command."""

    material_id: UUID
    name: str
    article: str | None
    unit: str
    description: str | None
