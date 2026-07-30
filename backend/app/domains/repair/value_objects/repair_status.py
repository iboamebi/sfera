"""
Repair status value object.
"""

from enum import StrEnum


class RepairStatus(StrEnum):
    """Repair lifecycle states."""

    NEW = "NEW"
    IN_WORK = "IN_WORK"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
