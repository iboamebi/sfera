from uuid import uuid4

from app.api.routers.site import create_site
from app.api.routers.site import get_organization_sites
from app.api.routers.site import get_site
from app.api.routers.site import get_sites
from app.domains.site.entities.site import Site
from app.schemas.site import SiteRead


def make_site() -> Site:
    """Build a Site entity for API router tests."""
    return Site(
        id=uuid4(),
        organization_id=uuid4(),
        name="Main site",
        address="Main street, 1",
        archived=False,
    )


def test_create_site_returns_api_contract() -> None:
    site = make_site()

    class FakeSiteService:
        def create(self, command: object, user: object) -> Site:
            assert command.organization_id == site.organization_id
            assert command.name == site.name
            assert command.address == site.address
            return site

    result = create_site(
        data=type(
            "SiteCreateData",
            (),
            {
                "organization_id": site.organization_id,
                "name": site.name,
                "address": site.address,
                "model_dump": lambda self: {
                    "organization_id": self.organization_id,
                    "name": self.name,
                    "address": self.address,
                },
            },
        )(),
        user=object(),
        service=FakeSiteService(),
    )

    assert result.id == site.id
    assert result.organization_id == site.organization_id
    assert result.name == site.name
    assert result.address == site.address
    assert result.archived is False


def test_get_site_returns_api_contract() -> None:
    site = make_site()

    class FakeSiteService:
        def get(self, requested_id: object) -> Site | None:
            assert requested_id == site.id
            return site

    result = get_site(
        site_id=site.id,
        service=FakeSiteService(),
    )

    assert result.id == site.id
    assert result.organization_id == site.organization_id
    assert result.name == site.name
    assert result.address == site.address


def test_get_site_raises_404_when_site_is_missing() -> None:
    from fastapi import HTTPException

    class FakeSiteService:
        def get(self, requested_id: object) -> Site | None:
            assert requested_id is not None
            return None

    try:
        get_site(
            site_id=uuid4(),
            service=FakeSiteService(),
        )
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Site not found"
    else:
        raise AssertionError("Expected HTTPException")


def test_get_sites_returns_sites() -> None:
    sites = [make_site(), make_site()]

    class FakeSiteService:
        def get_all(self) -> list[Site]:
            return sites

    result = get_sites(service=FakeSiteService())

    assert result is sites
    assert len(result) == 2


def test_get_organization_sites_returns_sites() -> None:
    organization_id = uuid4()
    sites = [make_site(), make_site()]

    class FakeSiteService:
        def get_by_organization_id(
            self,
            requested_organization_id: object,
        ) -> list[Site]:
            assert requested_organization_id == organization_id
            return sites

    result = get_organization_sites(
        organization_id=organization_id,
        service=FakeSiteService(),
    )

    assert result is sites
    assert len(result) == 2


def test_site_read_schema_maps_domain_entity() -> None:
    site = make_site()

    result = SiteRead.model_validate(site, from_attributes=True)

    assert result.id == site.id
    assert result.organization_id == site.organization_id
    assert result.name == site.name
    assert result.address == site.address
    assert result.archived is False
