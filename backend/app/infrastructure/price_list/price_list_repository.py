"""
SQLAlchemy implementation of PriceListRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.price_list.entities.price_list import PriceList
from app.domains.price_list.repositories.price_list_repository import (
    PriceListRepository,
)
from app.models.price_list import PriceList as PriceListModel


class PriceListRepositorySQLAlchemy(PriceListRepository):
    """
    SQLAlchemy repository for PriceList aggregate.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    async def get_by_id(
        self,
        price_list_id: UUID,
    ) -> PriceList | None:
        model = (
            self.db.query(PriceListModel)
            .filter(PriceListModel.id == price_list_id)
            .first()
        )

        if model is None:
            return None

        return self._to_domain(model)

    async def get_active(
        self,
    ) -> PriceList | None:
        model = (
            self.db.query(PriceListModel)
            .filter(PriceListModel.is_active.is_(True))
            .first()
        )

        if model is None:
            return None

        return self._to_domain(model)

    async def list(
        self,
    ) -> list[PriceList]:
        models = self.db.query(PriceListModel).all()

        return [self._to_domain(model) for model in models]

    async def save(
        self,
        price_list: PriceList,
    ) -> PriceList:
        model = (
            self.db.query(PriceListModel)
            .filter(PriceListModel.id == price_list.id)
            .first()
        )

        if model is None:
            raise ValueError("PriceList not found")

        model.name = price_list.name
        model.description = price_list.description
        model.is_active = price_list.is_active

        self.db.flush()

        return price_list

    async def delete(
        self,
        price_list_id: UUID,
    ) -> None:
        model = (
            self.db.query(PriceListModel)
            .filter(PriceListModel.id == price_list_id)
            .first()
        )

        if model is not None:
            self.db.delete(model)
            self.db.flush()

    def _to_domain(
        self,
        model: PriceListModel,
    ) -> PriceList:
        return PriceList(
            id=model.id,
            name=model.name,
            price_list_type="default",
            description=model.description,
            is_active=model.is_active,
        )
