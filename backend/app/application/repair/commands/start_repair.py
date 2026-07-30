"""
Start repair command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class StartRepairCommand:
    """Start repair request."""

    repair_id: UUID
