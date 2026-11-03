"""Tests for PriceList application service creation contracts."""

import asyncio
from decimal import Decimal
from uuid import UUID

from app.application.price_list.commands.add_price_list_item import (
    AddPriceListItemCommand,
)
from app.application.price_list.commands.create_price_list import (
    CreatePriceListCommand,
)
from app.application.price_list.services.price_list_application_service import (
    PriceListApplicationService,
)
from app.domains.price_list.entities.price_list import PriceList
from app.domains.price_list.repositories.price_list_repository import (
    PriceListRepository,
)


class FakePriceListRepository(PriceListRepository):
    def __init__(self) -> None:
        self.items: dict[UUID, PriceList] = {}

    async def get_by_id(self, price_list_id: UUID) -> PriceList | None:
        return self.items.get(price_list_id)

    async def get_active(self) -> PriceList | None:
        return next(
            (price_list for price_list in self.items.values() if price_list.is_active),
            None,
        )

    async def list(self) -> list[PriceList]:
        return list(self.items.values())

    async def save(self, price_list: PriceList) -> PriceList:
        self.items[price_list.id] = price_list
        return price_list

    async def delete(self, price_list_id: UUID) -> None:
        self.items.pop(price_list_id, None)


def test_create_generates_id_and_preserves_active_flag() -> None:
    repository = FakePriceListRepository()
    service = PriceListApplicationService(repository)

    price_list = asyncio.run(
        service.create(
            CreatePriceListCommand(
                name="Standard",
                price_list_type="GENERAL",
                is_active=True,
            )
        )
    )

    assert isinstance(price_list.id, UUID)
    assert price_list.is_active is True
    assert repository.items[price_list.id] is price_list


def test_add_item_generates_item_id() -> None:
    repository = FakePriceListRepository()
    service = PriceListApplicationService(repository)
    price_list = asyncio.run(
        service.create(
            CreatePriceListCommand(
                name="Standard",
                price_list_type="GENERAL",
            )
        )
    )

    result = asyncio.run(
        service.add_item(
            AddPriceListItemCommand(
                price_list_id=price_list.id,
                service_code="VER-001",
                name="Verification",
                price=Decimal("100.00"),
            )
        )
    )

    assert len(result.items) == 1
    assert isinstance(result.items[0].id, UUID)
    assert result.items[0].price == Decimal("100.00")
    assert repository.items[price_list.id] is result
