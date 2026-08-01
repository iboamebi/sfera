"""
Application service: Customer.
"""

from uuid import UUID, uuid4

from app.application.customer.commands.create_customer import (
    CreateCustomerCommand,
)
from app.application.customer.commands.update_customer import (
    UpdateCustomerCommand,
)
from app.application.customer.exceptions import (
    CustomerNotFoundApplicationError,
)
from app.domains.customer.entities.customer import Customer
from app.domains.customer.exceptions import CustomerNotFoundError
from app.domains.customer.repositories.customer_repository import (
    CustomerRepository,
)


class CustomerApplicationService:
    """Customer application service."""

    def __init__(
        self,
        repository: CustomerRepository,
    ) -> None:
        self._repository = repository

    def get(
        self,
        customer_id: UUID,
    ) -> Customer:
        """Get customer by identifier."""

        customer = self._repository.get(customer_id)

        if customer is None:
            raise CustomerNotFoundApplicationError from CustomerNotFoundError

        return customer

    def get_all(
        self,
    ) -> list[Customer]:
        """Get all customers."""

        return self._repository.get_all()

    def create(
        self,
        command: CreateCustomerCommand,
    ) -> Customer:
        """Create customer."""

        customer = Customer(
            id=uuid4(),
            organization_id=command.organization_id,
            name=command.name,
            contact_person=command.contact_person,
            phone=command.phone,
            email=command.email,
            comment=command.comment,
            discount_percent=command.discount_percent,
        )

        return self._repository.save(customer)

    def update(
        self,
        command: UpdateCustomerCommand,
    ) -> Customer:
        """Update customer."""

        customer = self.get(command.customer_id)

        if command.name is not None:
            customer.change_name(command.name)

        if command.contact_person is not None:
            customer.change_contact_person(
                command.contact_person,
            )

        if command.phone is not None:
            customer.change_phone(
                command.phone,
            )

        if command.email is not None:
            customer.change_email(
                command.email,
            )

        if command.comment is not None:
            customer.change_comment(
                command.comment,
            )

        if command.discount_percent is not None:
            customer.change_discount(
                command.discount_percent,
            )

        return self._repository.save(customer)

    def save(
        self,
        customer: Customer,
    ) -> Customer:
        """Save customer."""

        return self._repository.save(customer)

    def delete(
        self,
        customer_id: UUID,
    ) -> None:
        """Delete customer."""

        self._repository.delete(customer_id)
