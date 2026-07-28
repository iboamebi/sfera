# Get active PriceList query.
# Defines input data for retrieving the currently active PriceList.

from dataclasses import dataclass


@dataclass(frozen=True)
class GetActivePriceListQuery:
    """
    Query for retrieving active PriceList.
    """

    pass
