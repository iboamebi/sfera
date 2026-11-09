"""
Create customer command.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCustomerCommand:
    """Command for creating a customer."""

    name: str
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    comment: str | None = None
    discount_percent: float = 0.0
