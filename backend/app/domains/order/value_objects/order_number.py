from dataclasses import dataclass

from app.domains.order.exceptions import (
    InvalidOrderNumberDomainError,
)
from app.shared.base.value_object import ValueObject


@dataclass(frozen=True)
class OrderNumber(ValueObject):
    value: str

    def __post_init__(self) -> None:
        value = self.value.strip()

        if not value:
            raise InvalidOrderNumberDomainError

        object.__setattr__(self, "value", value)
