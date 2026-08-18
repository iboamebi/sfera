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
        include_archived: bool = False,
    ) -> Customer | None:
        """Get customer by identifier."""

        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        include_archived: bool = False,
    ) -> list[Customer]:
        """Get customers, excluding archived records by default."""

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        customer: Customer,
    ) -> Customer:
        """Save customer."""

        raise NotImplementedError
