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


class SqlAlchemyCustomerRepository(CustomerRepository):
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
    ) -> Customer | None:
        model = (
            self.session.query(CustomerModel)
            .filter(CustomerModel.id == customer_id)
            .first()
        )

        if model is None:
            return None

        return self.mapper.to_domain(model)

    def get_all(self) -> list[Customer]:
        models = self.session.query(CustomerModel).all()

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

    def delete(
        self,
        customer_id: UUID,
    ) -> None:
        model = (
            self.session.query(CustomerModel)
            .filter(CustomerModel.id == customer_id)
            .first()
        )

        if model is not None:
            self.session.delete(model)

        self.session.flush()
