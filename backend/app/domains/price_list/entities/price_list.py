# app/domains/price_list/entities/price_list.py
# PriceList aggregate root.

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from app.domains.price_list.entities.price_list_item import PriceListItem
from app.domains.price_list.exceptions import (
    InvalidPriceListNameError,
    PriceListAlreadyActiveError,
)
from app.shared.base.aggregate import AggregateRoot


@dataclass(eq=False, kw_only=True)
class PriceList(AggregateRoot):
    """
    Aggregate Root для управления прайс-листом.
    """

    name: str
    price_list_type: str

    currency: str = "RUB"
    description: str | None = None
    valid_from: date | None = None
    valid_to: date | None = None
    is_active: bool = False

    items: list[PriceListItem] = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise InvalidPriceListNameError()

    @classmethod
    def create(
        cls,
        *,
        name: str,
        price_list_type: str,
        currency: str = "RUB",
        valid_from: date | None = None,
        valid_to: date | None = None,
        description: str | None = None,
    ) -> PriceList:
        """
        Create a new price list aggregate.
        """

        return cls(
            name=name,
            price_list_type=price_list_type,
            currency=currency,
            valid_from=valid_from,
            valid_to=valid_to,
            description=description,
        )

    def activate(self) -> None:
        """
        Активирует прайс-лист.
        """

        if self.is_active:
            raise PriceListAlreadyActiveError()

        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """
        Деактивирует прайс-лист.
        """

        self.is_active = False
        self.updated_at = datetime.utcnow()

    def change_name(
        self,
        name: str,
    ) -> None:
        """
        Change price list name.
        """

        if not name.strip():
            raise InvalidPriceListNameError()

        self.name = name
        self.updated_at = datetime.utcnow()

    def change_price_list_type(
        self,
        price_list_type: str,
    ) -> None:
        """
        Change price list type.
        """

        self.price_list_type = price_list_type
        self.updated_at = datetime.utcnow()

    def change_currency(
        self,
        currency: str,
    ) -> None:
        """
        Change price list currency.
        """

        self.currency = currency
        self.updated_at = datetime.utcnow()

    def change_valid_period(
        self,
        valid_from: date | None,
        valid_to: date | None,
    ) -> None:
        """
        Change price list validity period.
        """

        self.valid_from = valid_from
        self.valid_to = valid_to
        self.updated_at = datetime.utcnow()

    def change_description(
        self,
        description: str | None,
    ) -> None:
        """
        Change price list description.
        """

        self.description = description
        self.updated_at = datetime.utcnow()

    def add_item(
        self,
        item: PriceListItem,
    ) -> None:
        """
        Добавляет позицию в прайс-лист.
        """

        self.items.append(item)
        self.updated_at = datetime.utcnow()

    def change_item_price(
        self,
        item_id: UUID,
        price: Decimal,
    ) -> None:
        """
        Change price list item price.
        """

        item = self.find_item_by_id(item_id)

        if item is None:
            raise ValueError(
                "Price list item not found",
            )

        item.update_price(price)

        self.updated_at = datetime.utcnow()

    def change_item_description(
        self,
        item_id: UUID,
        description: str | None,
    ) -> None:
        """
        Change price list item description.
        """

        item = self.find_item_by_id(item_id)

        if item is None:
            raise ValueError(
                "Price list item not found",
            )

        item.update_description(description)

        self.updated_at = datetime.utcnow()

    def remove_item(
        self,
        item_id: UUID,
    ) -> None:
        """
        Удаляет позицию из прайс-листа.
        """

        self.items = [item for item in self.items if item.id != item_id]

        self.updated_at = datetime.utcnow()

    def find_item_by_id(
        self,
        item_id: UUID,
    ) -> PriceListItem | None:
        """
        Поиск позиции по идентификатору.
        """

        for item in self.items:
            if item.id == item_id:
                return item

        return None

    def find_item_by_code(
        self,
        service_code: str,
    ) -> PriceListItem | None:
        """
        Поиск позиции по коду услуги.
        """

        for item in self.items:
            if item.service_code == service_code:
                return item

        return None
