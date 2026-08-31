"""
Update device command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateDeviceCommand:
    """Command for updating a device card."""

    device_id: UUID
    name: str
    serial_number: str
    registry_number: str | None = None
    modification: str | None = None
    manufacture_year: int | None = None
    inventory_number: str | None = None
    comment: str | None = None
