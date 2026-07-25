"""
Customer repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.customer.entities.customer import Customer


class CustomerRepository(ABC):
    """
    Abstract customer repository.
    """

    @abstractmethod
    def get_by_id(self, customer_id: UUID) -> Customer | None:
        """
        Get customer by identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        """
        Save customer.
        """
        raise NotImplementedError
