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
    def get_by_order_item_id(
        self,
        order_item_id: UUID,
    ) -> Order | None:
        """Get the order containing an order item."""
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
    ) -> list[Order]:
        """List orders."""
        raise NotImplementedError

    @abstractmethod
    def has_conflicting_order_for_instrument(
        self,
        instrument_id: UUID,
        exclude_order_id: UUID,
    ) -> bool:
        """Check whether an instrument belongs to another active order."""
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        order: Order,
    ) -> None:
        """Save order."""
        raise NotImplementedError
