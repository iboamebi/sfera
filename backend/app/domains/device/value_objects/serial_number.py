from dataclasses import dataclass

from app.domains.device.exceptions import (
    InvalidSerialNumberDomainError,
)
from app.shared.base.value_object import ValueObject


@dataclass(frozen=True)
class SerialNumber(ValueObject):
    value: str

    def __post_init__(self) -> None:
        value = self.value.strip()

        if not value:
            raise InvalidSerialNumberDomainError

        object.__setattr__(self, "value", value)
