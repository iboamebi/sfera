from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.application.organization.services.organization_application_service import (
    OrganizationApplicationService,
)
from app.core.dependencies.services import get_organization_service

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


class OrganizationCreate(BaseModel):
    name: str
    short_name: str | None = None
    inn: str | None = None
    kpp: str | None = None
    ogrn: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    comment: str | None = None


@router.post("/")
def create_organization(
    data: OrganizationCreate,
    service: OrganizationApplicationService = Depends(
        get_organization_service,
    ),
):
    return service.create(
        data.model_dump(),
    )


@router.get("/")
def get_organizations(
    service: OrganizationApplicationService = Depends(
        get_organization_service,
    ),
):
    return service.get_all()


@router.get("/{organization_id}")
def get_organization(
    organization_id: UUID,
    service: OrganizationApplicationService = Depends(
        get_organization_service,
    ),
):
    return service.get(
        organization_id,
    )
