"""
Domain entity: Customer.
"""

from dataclasses import dataclass
from uuid import UUID

from app.shared.base.entity import Entity


@dataclass(eq=False)
class Customer(Entity):
    """
    Customer domain entity.
    """

    organization_id: UUID
    name: str
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    comment: str | None = None
    discount_percent: float = 0.0

    def change_name(
        self,
        name: str,
    ) -> None:
        """Change customer name."""

        self.name = name

    def change_contact_person(
        self,
        contact_person: str | None,
    ) -> None:
        """Change customer contact person."""

        self.contact_person = contact_person

    def change_phone(
        self,
        phone: str | None,
    ) -> None:
        """Change customer phone."""

        self.phone = phone

    def change_email(
        self,
        email: str | None,
    ) -> None:
        """Change customer email."""

        self.email = email

    def change_comment(
        self,
        comment: str | None,
    ) -> None:
        """Change customer comment."""

        self.comment = comment

    def change_discount(
        self,
        discount_percent: float,
    ) -> None:
        """Change customer discount."""

        self.discount_percent = discount_percent
