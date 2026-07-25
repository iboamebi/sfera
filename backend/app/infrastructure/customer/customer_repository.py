"""
SQLAlchemy implementation of CustomerRepository.
"""

from uuid import UUID

from app.domains.customer.entities.customer import Customer
from app.domains.customer.repositories.customer_repository import (
    CustomerRepository,
)


class SqlAlchemyCustomerRepository(CustomerRepository):
    """
    SQLAlchemy customer repository.

    Temporary stub implementation.
    """

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        raise NotImplementedError

    def save(self, customer: Customer) -> Customer:
        raise NotImplementedError
