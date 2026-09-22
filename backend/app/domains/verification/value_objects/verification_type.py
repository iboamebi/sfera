"""Verification type value object."""

from enum import StrEnum


class VerificationType(StrEnum):
    """Classify the business reason for a verification."""

    PRIMARY = "PRIMARY"
    PERIODIC = "PERIODIC"
    AFTER_REPAIR = "AFTER_REPAIR"
