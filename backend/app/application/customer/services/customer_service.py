"""
Application service: Customer.
"""

from uuid import UUID

from app.domains.customer.entities.customer import Customer
from app.domains.customer.repositories.customer_repository import (
    CustomerRepository,
)


class CustomerService:
    """
    Customer application service.
    """

    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        """
        Return customer by identifier.
        """
        return self._repository.get_by_id(customer_id)

    def save(self, customer: Customer) -> Customer:
        """
        Save customer.
        """
        return self._repository.save(customer)
