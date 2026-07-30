"""
Create repair command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateRepairCommand:
    """Create repair request."""

    order_item_id: UUID
    description: str | None = None
