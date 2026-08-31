"""
Order read repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.order.read_models.order_read_models import OrderReadData


class OrderReadRepository(ABC):
    """Read repository for order details."""

    @abstractmethod
    def get(
        self,
        order_id: UUID,
    ) -> OrderReadData | None:
        """Get order read data."""
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[OrderReadData]:
        """List order read data."""
        raise NotImplementedError
