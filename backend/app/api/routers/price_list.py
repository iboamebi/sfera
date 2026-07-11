from app.api.base_router import BaseRouter
from app.crud.price_list import price_list_crud
from app.schemas.price_list import (
    PriceListCreate,
    PriceListRead,
    PriceListUpdate,
)

router = BaseRouter(
    crud=price_list_crud,
    read_schema=PriceListRead,
    create_schema=PriceListCreate,
    update_schema=PriceListUpdate,
    prefix="/price-lists",
    tags=["Price Lists"],
).router
