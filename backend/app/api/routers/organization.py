"""
Organization API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.organization.commands.create_organization import (
    CreateOrganizationCommand,
)
from app.application.organization.commands.update_organization import (
    UpdateOrganizationCommand,
)
from app.application.organization.exceptions import (
    OrganizationNotFoundApplicationError,
)
from app.application.organization.services.organization_application_service import (
    OrganizationApplicationService,
)
from app.core.dependencies.services import get_organization_service
from app.domains.user.entities.user import User
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationRead,
    OrganizationUpdate,
)

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post(
    "/",
    response_model=OrganizationRead,
    status_code=201,
)
def create_organization(
    data: OrganizationCreate,
    user: User = Depends(get_current_user),
    __: None = Depends(require_csrf),
    service: OrganizationApplicationService = Depends(
        get_organization_service,
    ),
):
    command = CreateOrganizationCommand(
        **data.model_dump(),
    )

    return service.create(command, user)


@router.get(
    "/",
    response_model=list[OrganizationRead],
)
def get_organizations(
    service: OrganizationApplicationService = Depends(
        get_organization_service,
    ),
):
    return service.get_all()


@router.get(
    "/{organization_id}",
    response_model=OrganizationRead,
)
def get_organization(
    organization_id: UUID,
    service: OrganizationApplicationService = Depends(
        get_organization_service,
    ),
):
    try:
        return service.get(organization_id)

    except OrganizationNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        ) from None


@router.patch(
    "/{organization_id}",
    response_model=OrganizationRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def update_organization(
    organization_id: UUID,
    data: OrganizationUpdate,
    service: OrganizationApplicationService = Depends(
        get_organization_service,
    ),
):
    command = UpdateOrganizationCommand(
        organization_id=organization_id,
        **data.model_dump(
            exclude_unset=True,
        ),
    )

    return service.update(command)
