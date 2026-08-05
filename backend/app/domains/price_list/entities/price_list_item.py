from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.domains.price_list.exceptions import InvalidPriceError
from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class PriceListItem(Entity):
    """
    Позиция прайс-листа.
    """

    service_code: str
    name: str
    price: Decimal

    unit: str = "pcs"
    description: str | None = None

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        self.validate_price()

    def validate_price(self) -> None:
        """
        Проверяет корректность стоимости.
        """

        if self.price < Decimal("0"):
            raise InvalidPriceError(self.price)

    def update_price(
        self,
        price: Decimal,
    ) -> None:
        """
        Изменяет стоимость позиции.
        """

        if price < Decimal("0"):
            raise InvalidPriceError(price)

        self.price = price
        self.updated_at = datetime.utcnow()

    def update_description(
        self,
        description: str | None,
    ) -> None:
        """
        Обновляет описание позиции.
        """

        self.description = description
        self.updated_at = datetime.utcnow()
