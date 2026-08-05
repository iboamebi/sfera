"""
Restore Material command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RestoreMaterialCommand:
    """Restore material command."""

    material_id: UUID
