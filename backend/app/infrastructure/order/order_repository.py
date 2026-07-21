from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.order.entities.order import Order as DomainOrder
from app.domains.order.repositories.order_repository import OrderRepository
from app.models.order import Order as ORMOrder


class OrderRepositorySQLAlchemy(OrderRepository):
    def __init__(self, db: Session):
        self.db = db

    def get(self, order_id: UUID) -> DomainOrder | None:
        obj = self.db.query(ORMOrder).filter(ORMOrder.id == order_id).first()

        if not obj:
            return None

        return DomainOrder(
            id=obj.id,
            number=obj.number,
            customer_id=obj.customer_id,
        )

    def save(self, order: DomainOrder) -> None:
        obj = self.db.query(ORMOrder).filter(ORMOrder.id == order.id).first()

        if obj:
            obj.number = order.number.value
            obj.status = order.status.value
        else:
            obj = ORMOrder(
                id=order.id,
                number=order.number.value,
                customer_id=order.customer_id,
                status=order.status.value,
            )

            self.db.add(obj)

        self.db.commit()
