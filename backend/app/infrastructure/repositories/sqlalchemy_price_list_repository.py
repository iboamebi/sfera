# backend/app/infrastructure/repositories/sqlalchemy_price_list_repository.py
# SQLAlchemy implementation of PriceList repository

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.price_list import PriceList


class SQLAlchemyPriceListRepository:
    """
    SQLAlchemy repository implementation for PriceList.
    """

    def __init__(self, db: Session):
        self.db = db

    def get(self, price_list_id: UUID):
        result = self.db.execute(select(PriceList).where(PriceList.id == price_list_id))
        return result.scalar_one_or_none()

    def get_all(self):
        result = self.db.execute(select(PriceList).where(PriceList.archived.is_(False)))
        return result.scalars().all()

    def create(self, data):
        obj = PriceList(**data.model_dump())

        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)

        return obj

    def update(self, price_list, data):
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(price_list, key, value)

        self.db.flush()
        self.db.refresh(price_list)

        return price_list
