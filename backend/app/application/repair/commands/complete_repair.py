"""
Complete repair command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CompleteRepairCommand:
    """Complete repair request."""

    repair_id: UUID
    result: str
