"""
Order repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.order.entities.order import Order


class OrderRepository(ABC):
    """Abstract order repository."""

    @abstractmethod
    def get(
        self,
        order_id: UUID,
    ) -> Order | None:
        """Get order by identifier."""
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
    ) -> list[Order]:
        """List orders."""
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        order: Order,
    ) -> None:
        """Save order."""
        raise NotImplementedError
