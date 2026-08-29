"""
Requested operations for an OrderItem.
"""

from enum import StrEnum


class OrderItemOperation(StrEnum):
    """Business operations that may be requested for an order item."""

    VERIFICATION = "verification"
    DIAGNOSTIC = "diagnostic"
    REPAIR = "repair"
    SALE = "sale"
