"""
Update customer command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateCustomerCommand:
    """Command for updating a customer."""

    customer_id: UUID

    name: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    comment: str | None = None
    discount_percent: float | None = None
