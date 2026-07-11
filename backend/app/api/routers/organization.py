from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.organization import Organization
from pydantic import BaseModel


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
    db: Session = Depends(get_db),
):
    organization = Organization(**data.model_dump())

    db.add(organization)
    db.commit()
    db.refresh(organization)

    return organization


@router.get("/")
def get_organizations(
    db: Session = Depends(get_db),
):
    return db.query(Organization).all()


@router.get("/{organization_id}")
def get_organization(
    organization_id: UUID,
    db: Session = Depends(get_db),
):
    return (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )
