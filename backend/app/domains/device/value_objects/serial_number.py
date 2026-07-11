from dataclasses import dataclass

from app.shared.base.value_object import ValueObject


@dataclass(frozen=True)
class SerialNumber(ValueObject):
    value: str

    def __post_init__(self):
        value = self.value.strip()

        if not value:
            raise ValueError("Serial number cannot be empty")

        object.__setattr__(self, "value", value)
