"""
Customer repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.customer.entities.customer import Customer


class CustomerRepository(ABC):
    """Abstract customer repository."""

    @abstractmethod
    def get(
        self,
        customer_id: UUID,
    ) -> Customer | None:
        """Get customer by identifier."""

        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
    ) -> list[Customer]:
        """Get all customers."""

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        customer: Customer,
    ) -> Customer:
        """Save customer."""

        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        customer_id: UUID,
    ) -> None:
        """Delete customer."""

        raise NotImplementedError
