"""
Tests for Site application service.
"""

from uuid import UUID, uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.site.commands.create_site import CreateSiteCommand
from app.application.site.services.site_application_service import (
    SiteApplicationService,
)
from app.domains.site.entities.site import Site
from app.domains.site.repositories.site_repository import SiteRepository
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    """Minimal unit of work double for application service tests."""

    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def register_aggregate(
        self,
        aggregate: object,
        operation_id: UUID | None = None,
    ) -> None:
        pass


class FakeSiteRepository(SiteRepository):
    """In-memory site repository for application service tests."""

    def __init__(self) -> None:
        self._sites: dict[UUID, Site] = {}

    def get(self, site_id: UUID) -> Site | None:
        return self._sites.get(site_id)

    def get_all(self) -> list[Site]:
        return list(self._sites.values())

    def get_by_organization_id(
        self,
        organization_id: UUID,
    ) -> list[Site]:
        return [
            site
            for site in self._sites.values()
            if site.organization_id == organization_id
        ]

    def save(self, site: Site) -> Site:
        self._sites[site.id] = site
        return site


def make_user(role: UserRole) -> User:
    """Build a user with the requested role."""

    return User(
        id=uuid4(),
        username=f"test-{role.value}",
        password_hash="hash",
        role=role,
    )


def test_create_site():
    repository = FakeSiteRepository()
    uow = FakeUnitOfWork()
    service = SiteApplicationService(repository, uow)
    organization_id = uuid4()

    site = service.create(
        CreateSiteCommand(
            organization_id=organization_id,
            name="Main site",
            address="Main street, 1",
        ),
        make_user(UserRole.OPERATOR),
    )

    assert site.id is not None
    assert site.organization_id == organization_id
    assert site.name == "Main site"
    assert site.address == "Main street, 1"
    assert site.archived is False
    assert repository.get(site.id) is site
    assert uow.committed is True
    assert uow.rolled_back is False


def test_create_site_rejects_unauthorized_user():
    repository = FakeSiteRepository()
    uow = FakeUnitOfWork()
    service = SiteApplicationService(repository, uow)

    with pytest.raises(AuthorizationError, match="not authorized"):
        service.create(
            CreateSiteCommand(
                organization_id=uuid4(),
                name="Protected site",
                address="Protected address",
            ),
            make_user(UserRole.WAREHOUSE),
        )

    assert repository.get_all() == []
    assert uow.committed is False
    assert uow.rolled_back is False


def test_get_site():
    repository = FakeSiteRepository()
    service = SiteApplicationService(repository, FakeUnitOfWork())
    site = Site(
        id=uuid4(),
        organization_id=uuid4(),
        name="Main site",
        address="Main street, 1",
    )
    repository.save(site)

    result = service.get(site.id)

    assert result is site


def test_get_all_sites():
    repository = FakeSiteRepository()
    service = SiteApplicationService(repository, FakeUnitOfWork())
    first = Site(
        id=uuid4(),
        organization_id=uuid4(),
        name="First site",
        address="First address",
    )
    second = Site(
        id=uuid4(),
        organization_id=uuid4(),
        name="Second site",
        address="Second address",
    )
    repository.save(first)
    repository.save(second)

    result = service.get_all()

    assert result == [first, second]


def test_get_sites_by_organization_id():
    repository = FakeSiteRepository()
    service = SiteApplicationService(repository, FakeUnitOfWork())
    organization_id = uuid4()
    matching = Site(
        id=uuid4(),
        organization_id=organization_id,
        name="Matching site",
        address="Matching address",
    )
    other = Site(
        id=uuid4(),
        organization_id=uuid4(),
        name="Other site",
        address="Other address",
    )
    repository.save(matching)
    repository.save(other)

    result = service.get_by_organization_id(organization_id)

    assert result == [matching]
