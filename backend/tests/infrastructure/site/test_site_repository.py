from uuid import uuid4

from app.domains.site.entities.site import Site
from app.infrastructure.site.site_repository import SiteRepositorySQLAlchemy
from app.models.site import Site as SiteModel


class FakeQuery:
    """Minimal query double for repository tests."""

    def __init__(self, models: list[SiteModel]) -> None:
        self.models = models

    def filter(self, *conditions: object) -> "FakeQuery":
        return self

    def first(self) -> SiteModel | None:
        return self.models[0] if self.models else None

    def all(self) -> list[SiteModel]:
        return self.models


class FakeSession:
    """Minimal session double for repository tests."""

    def __init__(self, models: list[SiteModel] | None = None) -> None:
        self.models = models or []
        self.added: list[object] = []
        self.flushed = False

    def query(self, model: type[SiteModel]) -> FakeQuery:
        return FakeQuery(self.models)

    def add(self, model: object) -> None:
        self.added.append(model)

    def flush(self) -> None:
        self.flushed = True


def make_site() -> Site:
    """Build a Site entity for repository tests."""
    return Site(
        id=uuid4(),
        organization_id=uuid4(),
        name="Main site",
        address="Main street, 1",
    )


def make_model(site: Site) -> SiteModel:
    """Build a Site ORM model for repository tests."""
    return SiteModel(
        id=site.id,
        organization_id=site.organization_id,
        name=site.name,
        address=site.address,
        archived=site.archived,
    )


def test_get_returns_site() -> None:
    site = make_site()
    model = make_model(site)
    session = FakeSession([model])

    result = SiteRepositorySQLAlchemy(session).get(site.id)

    assert result is not None
    assert result.id == site.id
    assert result.organization_id == site.organization_id
    assert result.name == site.name
    assert result.address == site.address


def test_get_returns_none_without_model() -> None:
    result = SiteRepositorySQLAlchemy(FakeSession()).get(uuid4())

    assert result is None


def test_get_all_returns_sites() -> None:
    first = make_site()
    second = make_site()
    session = FakeSession([make_model(first), make_model(second)])

    result = SiteRepositorySQLAlchemy(session).get_all()

    assert [site.id for site in result] == [first.id, second.id]


def test_get_by_organization_id_returns_sites() -> None:
    first = make_site()
    second = make_site()
    session = FakeSession([make_model(first), make_model(second)])

    result = SiteRepositorySQLAlchemy(session).get_by_organization_id(
        first.organization_id,
    )

    assert [site.id for site in result] == [first.id, second.id]


def test_save_creates_site() -> None:
    site = make_site()
    session = FakeSession()

    result = SiteRepositorySQLAlchemy(session).save(site)

    assert result.id == site.id
    assert len(session.added) == 1
    model = session.added[0]
    assert isinstance(model, SiteModel)
    assert model.organization_id == site.organization_id
    assert model.name == site.name
    assert model.address == site.address
    assert model.archived == site.archived
    assert session.flushed is True


def test_save_updates_existing_site() -> None:
    site = make_site()
    model = make_model(site)
    model.name = "Old site"
    session = FakeSession([model])

    result = SiteRepositorySQLAlchemy(session).save(site)

    assert result.id == site.id
    assert session.added == []
    assert model.name == site.name
    assert model.address == site.address
    assert session.flushed is True
