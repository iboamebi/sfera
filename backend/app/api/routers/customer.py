from app.api.base_router import BaseRouter
from app.crud.customer import customer_crud
from app.schemas.customer import (
    CustomerCreate,
    CustomerRead,
    CustomerUpdate,
)

router = BaseRouter(
    crud=customer_crud,
    read_schema=CustomerRead,
    create_schema=CustomerCreate,
    update_schema=CustomerUpdate,
    prefix="/customers",
    tags=["Customers"],
).router
