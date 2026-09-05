"""
Site API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.site.commands.create_site import CreateSiteCommand
from app.application.site.services.site_application_service import (
    SiteApplicationService,
)
from app.core.dependencies.services import get_site_service
from app.domains.user.entities.user import User
from app.schemas.site import SiteCreate, SiteRead

router = APIRouter(
    prefix="/sites",
    tags=["Sites"],
)


@router.get(
    "/",
    response_model=list[SiteRead],
)
def get_sites(
    service: SiteApplicationService = Depends(
        get_site_service,
    ),
):
    return service.get_all()


@router.get(
    "/organization/{organization_id}",
    response_model=list[SiteRead],
)
def get_organization_sites(
    organization_id: UUID,
    service: SiteApplicationService = Depends(
        get_site_service,
    ),
):
    return service.get_by_organization_id(organization_id)


@router.get(
    "/{site_id}",
    response_model=SiteRead,
)
def get_site(
    site_id: UUID,
    service: SiteApplicationService = Depends(
        get_site_service,
    ),
):
    site = service.get(site_id)
    if site is None:
        raise HTTPException(
            status_code=404,
            detail="Site not found",
        )
    return site


@router.post(
    "/",
    response_model=SiteRead,
    status_code=201,
)
def create_site(
    data: SiteCreate,
    user: User = Depends(get_current_user),
    __: None = Depends(require_csrf),
    service: SiteApplicationService = Depends(
        get_site_service,
    ),
):
    command = CreateSiteCommand(
        **data.model_dump(),
    )

    return service.create(command, user)
