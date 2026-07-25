"""
Domain entity: Customer.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class Customer:
    """
    Customer domain entity.
    """

    id: UUID
    organization_id: UUID
    name: str
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    comment: str | None = None
    discount_percent: float = 0.0
