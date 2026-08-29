"""
Update device command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateDeviceCommand:
    """Command for updating supplied device card fields."""

    device_id: UUID
    instrument_type_id: UUID | None = None
    serial_number: str | None = None
    registry_number: str | None = None
    modification: str | None = None
    factory_number: str | None = None
    manufacture_year: int | None = None
    inventory_number: str | None = None
    comment: str | None = None
