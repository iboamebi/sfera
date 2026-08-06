# app/application/price_list/commands/create_price_list.py
# Command for creating a new PriceList aggregate.

from dataclasses import dataclass


@dataclass(frozen=True)
class CreatePriceListCommand:
    """
    Command for creating a new PriceList.
    """

    name: str
    price_list_type: str
    description: str | None = None
    is_active: bool = True
