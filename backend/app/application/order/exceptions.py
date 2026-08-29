"""
Application exceptions for Order.
"""


class OrderNotFoundApplicationError(Exception):
    """Order not found application error."""


class OrderItemNotFoundApplicationError(Exception):
    """Order item not found application error."""


class InstrumentAlreadyInActiveOrderApplicationError(Exception):
    """Instrument already belongs to another active order."""
