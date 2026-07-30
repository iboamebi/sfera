"""
Cancel repair command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CancelRepairCommand:
    """Cancel repair request."""

    repair_id: UUID
