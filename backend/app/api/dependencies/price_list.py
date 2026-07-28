# backend/app/api/dependencies/price_list.py
# PriceList service dependency

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.price_list_service import PriceListService
from app.db.database import get_db
from app.infrastructure.repositories.sqlalchemy_price_list_repository import (
    SQLAlchemyPriceListRepository,
)


def get_price_list_service(
    db: Session = Depends(get_db),
) -> PriceListService:
    repository = SQLAlchemyPriceListRepository(db)

    return PriceListService(repository)
