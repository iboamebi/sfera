"""
Connect device command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ConnectDeviceCommand:
    """Command to connect a device."""

    device_id: UUID
