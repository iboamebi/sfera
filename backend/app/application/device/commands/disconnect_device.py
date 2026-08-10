"""
Disconnect device command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DisconnectDeviceCommand:
    """Command to disconnect a device."""

    device_id: UUID
