"""
Customer domain/model mapper.
"""

from app.domains.customer.entities.customer import Customer
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.customer import Customer as CustomerModel


class CustomerMapper(
    BaseMapper[
        Customer,
        CustomerModel,
    ],
):
    """Maps Customer between domain and SQLAlchemy model."""

    def to_domain(
        self,
        model: CustomerModel,
    ) -> Customer:
        """Convert ORM model to domain entity."""

        return Customer(
            id=model.id,
            organization_id=model.organization_id,
            name=model.name,
            contact_person=model.contact_person,
            phone=model.phone,
            email=model.email,
            comment=model.comment,
            discount_percent=float(model.discount_percent),
        )

    def to_model(
        self,
        entity: Customer,
        model: CustomerModel,
    ) -> CustomerModel:
        """Convert domain entity to ORM model."""

        model.organization_id = entity.organization_id
        model.name = entity.name
        model.contact_person = entity.contact_person
        model.phone = entity.phone
        model.email = entity.email
        model.comment = entity.comment
        model.discount_percent = entity.discount_percent

        return model
