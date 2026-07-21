from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.order.entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def get(self, order_id: UUID) -> Order | None:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass
