"""
Organization domain/model mapper.
"""

from app.domains.organization.entities.organization import Organization
from app.models.organization import Organization as OrganizationModel


class OrganizationMapper:
    """Maps Organization between domain and SQLAlchemy model."""

    def to_domain(
        self,
        model: OrganizationModel,
    ) -> Organization:
        """Convert ORM model to domain entity."""

        return Organization(
            id=model.id,
            name=model.name,
            short_name=model.short_name,
            inn=model.inn,
            kpp=model.kpp,
            ogrn=model.ogrn,
            address=model.address,
            phone=model.phone,
            email=model.email,
            website=model.website,
            comment=model.comment,
        )

    def to_model(
        self,
        entity: Organization,
        model: OrganizationModel,
    ) -> OrganizationModel:
        """Convert domain entity to ORM model."""

        model.name = entity.name
        model.short_name = entity.short_name
        model.inn = entity.inn
        model.kpp = entity.kpp
        model.ogrn = entity.ogrn
        model.address = entity.address
        model.phone = entity.phone
        model.email = entity.email
        model.website = entity.website
        model.comment = entity.comment

        return model
