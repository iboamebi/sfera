"""
Order read service.
"""

from uuid import UUID

from app.application.order.queries.order_read_mapper import (
    OrderReadMapper,
)
from app.domains.order.repositories.order_read_repository import (
    OrderReadRepository,
)
from app.schemas.order import OrderRead


class OrderReadService:
    """Provides order read operations."""

    def __init__(
        self,
        repository: OrderReadRepository,
    ) -> None:
        self._repository = repository
        self._mapper = OrderReadMapper()

    def get(
        self,
        order_id: UUID,
    ) -> OrderRead | None:
        model = self._repository.get(order_id)

        if model is None:
            return None

        return self._mapper.to_schema(model)
