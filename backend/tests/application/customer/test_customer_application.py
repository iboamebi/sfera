"""
Tests for Customer application service.
"""

from uuid import UUID, uuid4

from app.application.customer.commands.create_customer import (
    CreateCustomerCommand,
)
from app.application.customer.commands.delete_customer import (
    DeleteCustomerCommand,
)
from app.application.customer.commands.update_customer import (
    UpdateCustomerCommand,
)
from app.application.customer.services.customer_application_service import (
    CustomerApplicationService,
)
from app.domains.customer.entities.customer import Customer
from app.domains.customer.repositories.customer_repository import (
    CustomerRepository,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class FakeCustomerRepository(CustomerRepository):
    def __init__(self) -> None:
        self._customers: dict[UUID, Customer] = {}

    def get(self, customer_id: UUID) -> Customer | None:
        return self._customers.get(customer_id)

    def get_all(self) -> list[Customer]:
        return list(self._customers.values())

    def save(self, customer: Customer) -> Customer:
        self._customers[customer.id] = customer
        return customer

    def delete(self, customer_id: UUID) -> None:
        self._customers.pop(customer_id, None)


def test_create_customer():
    repository = FakeCustomerRepository()
    service = CustomerApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    organization_id = uuid4()

    customer = service.create(
        CreateCustomerCommand(
            organization_id=organization_id,
            name="Sfera Test Customer",
            contact_person="Test Person",
            phone="+7 900 000-00-00",
            email="test@example.com",
            comment="Test customer",
            discount_percent=5.5,
        )
    )

    assert customer.id is not None
    assert customer.organization_id == organization_id
    assert customer.name == "Sfera Test Customer"
    assert customer.contact_person == "Test Person"
    assert customer.phone == "+7 900 000-00-00"
    assert customer.email == "test@example.com"
    assert customer.comment == "Test customer"
    assert customer.discount_percent == 5.5
    assert customer.archived is False
    assert repository.get(customer.id) is customer


def test_update_customer():
    repository = FakeCustomerRepository()
    service = CustomerApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    customer = service.create(
        CreateCustomerCommand(
            organization_id=uuid4(),
            name="Original Customer",
        )
    )

    updated = service.update(
        UpdateCustomerCommand(
            customer_id=customer.id,
            name="Updated Customer",
            contact_person="Updated Person",
            phone="+7 901 111-11-11",
            email="updated@example.com",
            comment="Updated customer",
            discount_percent=10.0,
        )
    )

    assert updated.id == customer.id
    assert updated.name == "Updated Customer"
    assert updated.contact_person == "Updated Person"
    assert updated.phone == "+7 901 111-11-11"
    assert updated.email == "updated@example.com"
    assert updated.comment == "Updated customer"
    assert updated.discount_percent == 10.0
    assert repository.get(customer.id) is updated


def test_delete_customer():
    repository = FakeCustomerRepository()
    service = CustomerApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    customer = service.create(
        CreateCustomerCommand(
            organization_id=uuid4(),
            name="Customer to Delete",
        )
    )

    service.delete(
        DeleteCustomerCommand(
            customer_id=customer.id,
        )
    )

    assert repository.get(customer.id) is None
