"""
Archive Material command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ArchiveMaterialCommand:
    """Archive material command."""

    material_id: UUID
