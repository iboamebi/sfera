"""
Command: update instrument type.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateInstrumentTypeCommand:
    """Update instrument type command."""

    instrument_type_id: UUID
    name: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    measurement_type: str | None = None
    accuracy_class: str | None = None
    verification_interval_months: int | None = None
    description: str | None = None
