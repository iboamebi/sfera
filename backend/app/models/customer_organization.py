import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class CustomerOrganization(BaseModel):
    """ORM association between a customer and an organization."""

    __tablename__ = "customer_organizations"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
    )

    customer = relationship(
        "Customer",
        back_populates="customer_organizations",
    )

    organization = relationship(
        "Organization",
        back_populates="customer_organizations",
    )
