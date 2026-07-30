"""
Update Material command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateMaterialCommand:
    """Update material command."""

    material_id: UUID
    name: str | None = None
    article: str | None = None
    unit: str | None = None
    description: str | None = None
