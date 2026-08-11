"""
Create warehouse command.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateWarehouseCommand:
    """Create warehouse command."""

    name: str
    address: str | None = None
    responsible_person: str | None = None
    comment: str | None = None
