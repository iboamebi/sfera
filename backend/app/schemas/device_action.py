"""
Device action API schemas.

Defines HTTP response contracts for device business actions.
Version: 1.0
Revision: 2026-08-11
"""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class DeviceActionResponse(BaseModel):
    """HTTP response for a device connection state action."""

    event: Literal[
        "DeviceConnected",
        "DeviceDisconnected",
    ]
    device_id: UUID
