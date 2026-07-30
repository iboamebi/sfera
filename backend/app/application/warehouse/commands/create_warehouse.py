"""
Create warehouse command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateWarehouseCommand:
    """Create warehouse command."""

    warehouse_id: UUID
    name: str
    address: str | None = None
    responsible_person: str | None = None
    comment: str | None = None
