"""
Create device command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateDeviceCommand:
    """Command for creating a device."""

    instrument_type_id: UUID
    name: str
    serial_number: str
