"""
Update diagnostic conclusion command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateConclusionCommand:
    """Update diagnostic conclusion data."""

    diagnostic_id: UUID
    conclusion: str
