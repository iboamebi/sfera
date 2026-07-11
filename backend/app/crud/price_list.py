from app.crud.base import BaseCRUD
from app.models.price_list import PriceList
from app.schemas.price_list import (
    PriceListCreate,
    PriceListUpdate,
)


class PriceListCRUD(
    BaseCRUD[
        PriceList,
        PriceListCreate,
        PriceListUpdate,
    ]
):
    pass


price_list_crud = PriceListCRUD(PriceList)
