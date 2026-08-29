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
    def has_conflicting_order_for_instrument(
        self,
        instrument_id: UUID,
        exclude_order_id: UUID,
    ) -> bool:
        """Check whether an instrument belongs to another active order."""
        raise NotImplementedError

    @abstractmethod
    def delete_item(
        self,
        order_id: UUID,
        item_id: UUID,
    ) -> bool:
        """Delete an order item and renumber remaining items."""
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        order: Order,
    ) -> None:
        """Save order."""
        raise NotImplementedError
