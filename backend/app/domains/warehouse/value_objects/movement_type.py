"""
Warehouse movement type value object.
"""

from enum import StrEnum


class MovementType(StrEnum):
    """Warehouse movement types."""

    RECEIPT = "RECEIPT"
    ISSUE = "ISSUE"
    RESERVATION = "RESERVATION"
    RELEASE = "RELEASE"
    ADJUSTMENT = "ADJUSTMENT"
