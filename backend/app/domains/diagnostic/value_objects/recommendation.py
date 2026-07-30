"""
Diagnostic recommendation value object.
"""

from enum import StrEnum


class Recommendation(StrEnum):
    """Diagnostic recommendations."""

    NO_ISSUES = "NO_ISSUES"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    REPLACEMENT_RECOMMENDED = "REPLACEMENT_RECOMMENDED"
    REPAIR_NOT_ECONOMIC = "REPAIR_NOT_ECONOMIC"
    WRITE_OFF = "WRITE_OFF"
    RETURN_TO_MANUFACTURER = "RETURN_TO_MANUFACTURER"
