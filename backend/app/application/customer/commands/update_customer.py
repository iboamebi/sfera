"""
Update customer command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class _Unset:
    """Marker for an update field that was not provided."""


UNSET = _Unset()


@dataclass(frozen=True)
class UpdateCustomerCommand:
    """Command for updating a customer."""

    customer_id: UUID

    name: str | None | _Unset = UNSET
    contact_person: str | None | _Unset = UNSET
    phone: str | None | _Unset = UNSET
    email: str | None | _Unset = UNSET
    comment: str | None | _Unset = UNSET
    discount_percent: float | None | _Unset = UNSET
