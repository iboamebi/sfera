"""
Command: create instrument type.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateInstrumentTypeCommand:
    """Create instrument type command."""

    name: str
    manufacturer: str | None = None
    model: str | None = None
    measurement_type: str | None = None
    accuracy_class: str | None = None
    verification_interval_months: int | None = None
    description: str | None = None
