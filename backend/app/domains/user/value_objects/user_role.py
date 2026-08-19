"""
User role value object.
"""

from enum import StrEnum


class UserRole(StrEnum):
    """Roles defined by the initial authorization business contract."""

    ADMIN = "admin"
    OPERATOR = "operator"
    METROLOGIST = "metrologist"
    TECHNICIAN = "technician"
    WAREHOUSE = "warehouse"
