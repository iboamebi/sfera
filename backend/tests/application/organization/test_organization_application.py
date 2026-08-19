"""
Tests for Organization application service.
"""

from uuid import UUID, uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.organization.commands.create_organization import (
    CreateOrganizationCommand,
)
from app.application.organization.commands.update_organization import (
    UpdateOrganizationCommand,
)
from app.application.organization.services.organization_application_service import (
    OrganizationApplicationService,
)
from app.domains.organization.entities.organization import Organization
from app.domains.organization.repositories.organization_repository import (
    OrganizationRepository,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class FakeOrganizationRepository(OrganizationRepository):
    def __init__(self) -> None:
        self._organizations: dict[UUID, Organization] = {}

    def get(self, organization_id: UUID) -> Organization | None:
        return self._organizations.get(organization_id)

    def get_all(self) -> list[Organization]:
        return list(self._organizations.values())

    def save(self, organization: Organization) -> Organization:
        self._organizations[organization.id] = organization
        return organization


def make_operator() -> User:
    return User(
        id=uuid4(),
        username="test-operator",
        password_hash="hash",
        role=UserRole.OPERATOR,
    )


def test_create_organization():
    repository = FakeOrganizationRepository()
    service = OrganizationApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    organization = service.create(
        CreateOrganizationCommand(
            name="Sfera Test Organization",
            short_name="Sfera",
            inn="1234567890",
            kpp="123456789",
            ogrn="1234567890123",
            address="Test address",
            phone="+7 900 000-00-00",
            email="test@example.com",
            website="https://example.com",
            comment="Test organization",
        ),
        make_operator(),
    )

    assert organization.id is not None
    assert organization.name == "Sfera Test Organization"
    assert organization.short_name == "Sfera"
    assert organization.inn == "1234567890"
    assert organization.kpp == "123456789"
    assert organization.ogrn == "1234567890123"
    assert organization.address == "Test address"
    assert organization.phone == "+7 900 000-00-00"
    assert organization.email == "test@example.com"
    assert organization.website == "https://example.com"
    assert organization.comment == "Test organization"
    assert repository.get(organization.id) is organization


def test_create_organization_rejects_unauthorized_user():
    repository = FakeOrganizationRepository()
    service = OrganizationApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    user = User(
        id=uuid4(),
        username="test-user",
        password_hash="hash",
        role=UserRole.WAREHOUSE,
    )

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.create(
            CreateOrganizationCommand(
                name="Unauthorized Organization",
            ),
            user,
        )

    assert repository.get_all() == []


def test_update_organization():
    repository = FakeOrganizationRepository()
    service = OrganizationApplicationService(
        repository,
        FakeUnitOfWork(),
    )

    organization = service.create(
        CreateOrganizationCommand(
            name="Original Organization",
        ),
        make_operator(),
    )

    updated = service.update(
        UpdateOrganizationCommand(
            organization_id=organization.id,
            name="Updated Organization",
            short_name="Updated",
            inn="9876543210",
            kpp="987654321",
            ogrn="9876543210987",
            address="Updated address",
            phone="+7 901 111-11-11",
            email="updated@example.com",
            website="https://updated.example.com",
            comment="Updated organization",
        )
    )

    assert updated.id == organization.id
    assert updated.name == "Updated Organization"
    assert updated.short_name == "Updated"
    assert updated.inn == "9876543210"
    assert updated.kpp == "987654321"
    assert updated.ogrn == "9876543210987"
    assert updated.address == "Updated address"
    assert updated.phone == "+7 901 111-11-11"
    assert updated.email == "updated@example.com"
    assert updated.website == "https://updated.example.com"
    assert updated.comment == "Updated organization"
    assert repository.get(organization.id) is updated
