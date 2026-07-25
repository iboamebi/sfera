from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.application.customer.services.customer_application_service import (
    CustomerApplicationService,
)
from app.core.dependencies.services import get_customer_service
from app.domains.customer.entities.customer import Customer
from app.schemas.customer import (
    CustomerCreate,
    CustomerRead,
    CustomerUpdate,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get(
    "/",
    response_model=list[CustomerRead],
)
def get_customers(
    service: CustomerApplicationService = Depends(
        get_customer_service,
    ),
):
    return service.get_all()


@router.get(
    "/{customer_id}",
    response_model=CustomerRead,
)
def get_customer(
    customer_id: UUID,
    service: CustomerApplicationService = Depends(
        get_customer_service,
    ),
):
    try:
        return service.get(customer_id)

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from None


@router.post(
    "/",
    response_model=CustomerRead,
    status_code=201,
)
def create_customer(
    data: CustomerCreate,
    service: CustomerApplicationService = Depends(
        get_customer_service,
    ),
):
    customer = Customer(
        id=uuid4(),
        organization_id=data.organization_id,
        name=data.name,
        contact_person=data.contact_person,
        phone=data.phone,
        email=data.email,
        comment=data.comment,
        discount_percent=data.discount_percent,
    )

    return service.save(customer)


@router.delete(
    "/{customer_id}",
    status_code=204,
)
def delete_customer(
    customer_id: UUID,
    service: CustomerApplicationService = Depends(
        get_customer_service,
    ),
):
    service.delete(customer_id)


@router.patch(
    "/{customer_id}",
    response_model=CustomerRead,
)
def update_customer(
    customer_id: UUID,
    data: CustomerUpdate,
    service: CustomerApplicationService = Depends(
        get_customer_service,
    ),
):
    customer = service.get(customer_id)

    for key, value in data.model_dump(
        exclude_unset=True,
    ).items():
        setattr(customer, key, value)

    return service.save(customer)
