from uuid import UUID

from app.crud.price_list import price_list_crud
from app.schemas.price_list import (
    PriceListCreate,
    PriceListUpdate,
)


class PriceListService:
    def __init__(self):
        self.crud = price_list_crud

    async def create(
        self,
        data: PriceListCreate,
    ):
        return await self.crud.create(data)

    async def get(
        self,
        price_list_id: UUID,
    ):
        return await self.crud.get(price_list_id)

    async def update(
        self,
        price_list_id: UUID,
        data: PriceListUpdate,
    ):
        return await self.crud.update(
            price_list_id,
            data,
        )

    async def delete(
        self,
        price_list_id: UUID,
    ):
        return await self.crud.delete(price_list_id)


price_list_service = PriceListService()
