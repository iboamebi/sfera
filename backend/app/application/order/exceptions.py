"""
Application exceptions for Order.
"""


class OrderNotFoundApplicationError(Exception):
    """Order not found application error."""


class InstrumentAlreadyInActiveOrderApplicationError(Exception):
    """Instrument already belongs to another active order."""


class InstrumentCustomerMismatchApplicationError(Exception):
    """Instrument does not belong to the order customer."""
