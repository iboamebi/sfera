"""
Customer domain exceptions.
"""


class CustomerError(Exception):
    """Base customer domain exception."""


class CustomerNotFoundError(CustomerError):
    """Raised when customer is not found."""
