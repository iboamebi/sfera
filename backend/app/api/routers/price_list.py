# backend/app/api/routers/price_list.py
# PriceList API router

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.services.price_list_service import PriceListService
from app.db.database import get_db
from app.infrastructure.repositories.sqlalchemy_price_list_repository import (
    SQLAlchemyPriceListRepository,
)
from app.schemas.price_list import (
    PriceListCreate,
    PriceListRead,
    PriceListUpdate,
)

router = APIRouter(
    prefix="/price-lists",
    tags=["Price Lists"],
)


def get_price_list_service(
    db: Session = Depends(get_db),
):
    repository = SQLAlchemyPriceListRepository(db)
    return PriceListService(repository)


@router.get("/", response_model=list[PriceListRead])
def get_all(
    service: PriceListService = Depends(get_price_list_service),
):
    return service.get_price_lists()


@router.get("/{obj_id}", response_model=PriceListRead)
def get_one(
    obj_id: UUID,
    service: PriceListService = Depends(get_price_list_service),
):
    obj = service.get_price_list(obj_id)

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Object not found",
        )

    return obj


@router.post("/", response_model=PriceListRead, status_code=201)
def create(
    data: PriceListCreate,
    service: PriceListService = Depends(get_price_list_service),
):
    return service.create_price_list(data)


@router.patch("/{obj_id}", response_model=PriceListRead)
def update(
    obj_id: UUID,
    data: PriceListUpdate,
    service: PriceListService = Depends(get_price_list_service),
):
    obj = service.update_price_list(obj_id, data)

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Object not found",
        )

    return obj
