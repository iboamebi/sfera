"""
Domain exceptions for Order.
"""


class OrderDomainError(Exception):
    """Base order domain error."""


class InvalidOrderNumberDomainError(OrderDomainError):
    """Order number is invalid."""
