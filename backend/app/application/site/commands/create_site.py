"""
Create site command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateSiteCommand:
    """Command for creating a site."""

    organization_id: UUID
    name: str
    address: str
