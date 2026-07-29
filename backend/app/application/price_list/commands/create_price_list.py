# Create PriceList command.
# Defines input data for creating a new PriceList aggregate.

from dataclasses import dataclass


@dataclass(frozen=True)
class CreatePriceListCommand:
    """
    Command for creating a new PriceList.
    """

    name: str
    description: str | None = None
    is_active: bool = True
