from dataclasses import dataclass

from app.shared.base.value_object import ValueObject


@dataclass(frozen=True)
class OrderNumber(ValueObject):
    value: str

    def __post_init__(self):
        value = self.value.strip()

        if not value:
            raise ValueError("Order number is empty")

        object.__setattr__(self, "value", value)
