"""Change an instrument's assigned site command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangeDeviceSiteCommand:
    """Command for a documented Site assignment change."""

    device_id: UUID
    site_id: UUID | None
    reason: str
