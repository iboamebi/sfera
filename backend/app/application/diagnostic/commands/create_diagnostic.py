"""
Create diagnostic command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateDiagnosticCommand:
    """Create diagnostic data."""

    order_item_id: UUID
