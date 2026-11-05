from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.customer.commands.create_customer import (
    CreateCustomerCommand,
)
from app.application.customer.commands.delete_customer import (
    DeleteCustomerCommand,
)
from app.application.customer.commands.add_customer_organization import (
    AddCustomerOrganizationCommand,
)
from app.application.customer.commands.unlink_customer_organization import (
    UnlinkCustomerOrganizationCommand,
)
from app.application.customer.commands.update_customer import (
    UpdateCustomerCommand,
)
from app.application.customer.customer_organization_exceptions import (
    CustomerOrganizationAlreadyLinkedApplicationError,
    CustomerOrganizationLinkNotFoundApplicationError,
    CustomerOrganizationNotFoundApplicationError,
)
from app.application.customer.exceptions import (
    CustomerNotFoundApplicationError,
)
from app.application.customer.services.customer_application_service import (
    CustomerApplicationService,
)
from app.application.customer.services.customer_organization_application_service import (
    CustomerOrganizationApplicationService,
)
from app.core.dependencies.services import (
    get_customer_organization_service,
    get_customer_service,
)
from app.domains.user.entities.user import User
from app.schemas.customer import (
    CustomerCreate,
    CustomerRead,
    CustomerUpdate,
)
from app.schemas.organization import OrganizationRead

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
    user: User = Depends(get_current_user),
    __: None = Depends(require_csrf),
    service: CustomerApplicationService = Depends(
        get_customer_service,
    ),
):
    command = CreateCustomerCommand(
        name=data.name,
        contact_person=data.contact_person,
        phone=data.phone,
        email=data.email,
        comment=data.comment,
        discount_percent=data.discount_percent,
    )

    return service.create(command, user)


@router.delete(
    "/{customer_id}",
    status_code=204,
)
def delete_customer(
    customer_id: UUID,
    user: User = Depends(get_current_user),
    __: None = Depends(require_csrf),
    service: CustomerApplicationService = Depends(
        get_customer_service,
    ),
):
    service.delete(
        DeleteCustomerCommand(
            customer_id=customer_id,
        ),
        user,
    )


@router.patch(
    "/{customer_id}",
    response_model=CustomerRead,
)
def update_customer(
    customer_id: UUID,
    data: CustomerUpdate,
    user: User = Depends(get_current_user),
    __: None = Depends(require_csrf),
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

    return service.update(command, user)


@router.get(
    "/{customer_id}/organizations",
    response_model=list[OrganizationRead],
)
def get_customer_organizations(
    customer_id: UUID,
    service: CustomerOrganizationApplicationService = Depends(
        get_customer_organization_service,
    ),
):
    try:
        return service.get_organizations(customer_id)
    except CustomerOrganizationNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Customer or organization not found",
        ) from None


@router.post(
    "/{customer_id}/organizations/{organization_id}",
    response_model=OrganizationRead,
    status_code=201,
)
def add_customer_organization(
    customer_id: UUID,
    organization_id: UUID,
    user: User = Depends(get_current_user),
    __: None = Depends(require_csrf),
    service: CustomerOrganizationApplicationService = Depends(
        get_customer_organization_service,
    ),
):
    try:
        return service.add(
            AddCustomerOrganizationCommand(
                customer_id=customer_id,
                organization_id=organization_id,
            ),
            user,
        )
    except CustomerOrganizationNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Customer or organization not found",
        ) from None
    except CustomerOrganizationAlreadyLinkedApplicationError:
        raise HTTPException(
            status_code=409,
            detail="Organization is already linked to customer",
        ) from None


@router.post(
    "/{customer_id}/organizations/{organization_id}/unlink",
    status_code=204,
)
def unlink_customer_organization(
    customer_id: UUID,
    organization_id: UUID,
    user: User = Depends(get_current_user),
    __: None = Depends(require_csrf),
    service: CustomerOrganizationApplicationService = Depends(
        get_customer_organization_service,
    ),
):
    try:
        service.unlink(
            UnlinkCustomerOrganizationCommand(
                customer_id=customer_id,
                organization_id=organization_id,
            ),
            user,
        )
    except CustomerOrganizationNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from None
    except CustomerOrganizationLinkNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Organization is not linked to customer",
        ) from None
