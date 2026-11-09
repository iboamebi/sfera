from uuid import uuid4

from app.domains.site.entities.site import Site
from app.infrastructure.mappers.site_mapper import SiteMapper
from app.models.site import Site as SiteModel


def make_site(*, archived: bool = False) -> Site:
    """Build a Site entity for mapper tests."""
    return Site(
        id=uuid4(),
        customer_id=uuid4(),
        name="Main site",
        address="Main street, 1",
        archived=archived,
    )


def test_to_domain_maps_site_fields() -> None:
    site_id = uuid4()
    customer_id = uuid4()
    model = SiteModel(
        id=site_id,
        customer_id=customer_id,
        name="Main site",
        address="Main street, 1",
        archived=True,
    )

    result = SiteMapper().to_domain(model)

    assert result.id == site_id
    assert result.customer_id == customer_id
    assert result.name == model.name
    assert result.address == model.address
    assert result.archived is True


def test_to_model_maps_site_fields() -> None:
    entity = make_site(archived=True)
    model = SiteModel(
        id=entity.id,
        customer_id=uuid4(),
        name="Old site",
        address="Old address",
        archived=False,
    )

    result = SiteMapper().to_model(entity, model)

    assert result is model
    assert model.customer_id == entity.customer_id
    assert model.name == entity.name
    assert model.address == entity.address
    assert model.archived is True
