from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4

from app.domains.price_list.entities.price_list_item import PriceListItem
from app.domains.price_list.exceptions import (
    InvalidPriceListNameError,
    PriceListAlreadyActiveError,
)
from app.shared.domain.base import AggregateRoot


@dataclass
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

    id: UUID = field(default_factory=uuid4)
    items: list[PriceListItem] = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.name.strip():
            raise InvalidPriceListNameError()

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

    def add_item(
        self,
        item: PriceListItem,
    ) -> None:
        """
        Добавляет позицию в прайс-лист.
        """

        self.items.append(item)
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
