from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.customer.commands.create_customer import (
    CreateCustomerCommand,
)
from app.application.customer.commands.delete_customer import (
    DeleteCustomerCommand,
)
from app.application.customer.commands.update_customer import (
    UpdateCustomerCommand,
)
from app.application.customer.exceptions import (
    CustomerNotFoundApplicationError,
)
from app.application.customer.services.customer_application_service import (
    CustomerApplicationService,
)
from app.core.dependencies.services import get_customer_service
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

    except CustomerNotFoundApplicationError:
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
    command = CreateCustomerCommand(
        organization_id=data.organization_id,
        name=data.name,
        contact_person=data.contact_person,
        phone=data.phone,
        email=data.email,
        comment=data.comment,
        discount_percent=data.discount_percent,
    )

    return service.create(command)


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
    service.delete(
        DeleteCustomerCommand(
            customer_id=customer_id,
        ),
    )


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
    command = UpdateCustomerCommand(
        customer_id=customer_id,
        **data.model_dump(
            exclude_unset=True,
        ),
    )

    return service.update(command)
