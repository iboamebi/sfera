from app.crud.base import BaseCRUD
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerCRUD(
    BaseCRUD[
        Customer,
        CustomerCreate,
        CustomerUpdate,
    ]
):
    pass


customer_crud = CustomerCRUD(Customer)
