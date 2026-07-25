"""
Application service: Customer.
"""

from uuid import UUID

from app.domains.customer.entities.customer import Customer
from app.domains.customer.repositories.customer_repository import (
    CustomerRepository,
)


class CustomerApplicationService:
    """Customer application service."""

    def __init__(
        self,
        repository: CustomerRepository,
    ) -> None:
        self._repository = repository

    def get(
        self,
        customer_id: UUID,
    ) -> Customer:
        """Get customer by identifier."""

        customer = self._repository.get(customer_id)

        if customer is None:
            raise ValueError("Customer not found")

        return customer

    def get_all(self) -> list[Customer]:
        """Get all customers."""

        return self._repository.get_all()

    def save(
        self,
        customer: Customer,
    ) -> Customer:
        """Save customer."""

        return self._repository.save(customer)

    def delete(
        self,
        customer_id: UUID,
    ) -> None:
        """Delete customer."""

        self._repository.delete(customer_id)
