"""
SQLAlchemy implementation of CustomerRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.customer.entities.customer import Customer
from app.domains.customer.repositories.customer_repository import (
    CustomerRepository,
)
from app.infrastructure.mappers.customer_mapper import CustomerMapper
from app.models.customer import Customer as CustomerModel


class CustomerRepositorySQLAlchemy(CustomerRepository):
    """SQLAlchemy customer repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session
        self.mapper = CustomerMapper()

    def get(
        self,
        customer_id: UUID,
        include_archived: bool = False,
    ) -> Customer | None:
        query = self.session.query(CustomerModel).filter(
            CustomerModel.id == customer_id,
        )

        if not include_archived:
            query = query.filter(CustomerModel.archived.is_(False))

        model = query.first()

        if model is None:
            return None

        return self.mapper.to_domain(model)

    def get_all(
        self,
        include_archived: bool = False,
    ) -> list[Customer]:
        query = self.session.query(CustomerModel)

        if not include_archived:
            query = query.filter(CustomerModel.archived.is_(False))

        models = query.all()

        return [self.mapper.to_domain(model) for model in models]

    def save(
        self,
        customer: Customer,
    ) -> Customer:
        model = (
            self.session.query(CustomerModel)
            .filter(CustomerModel.id == customer.id)
            .first()
        )

        if model is None:
            model = CustomerModel(
                id=customer.id,
            )
            self.session.add(model)

        self.mapper.to_model(
            customer,
            model,
        )

        self.session.flush()

        return customer
