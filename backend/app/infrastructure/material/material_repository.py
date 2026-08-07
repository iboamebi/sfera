"""
SQLAlchemy implementation of MaterialRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.material.entities.material import (
    Material as DomainMaterial,
)
from app.domains.material.repositories.material_repository import (
    MaterialRepository,
)
from app.infrastructure.mappers.material_mapper import MaterialMapper
from app.models.material import Material as MaterialModel


class MaterialRepositorySQLAlchemy(MaterialRepository):
    """SQLAlchemy material repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session
        self._mapper = MaterialMapper()

    def get(
        self,
        material_id: UUID,
    ) -> DomainMaterial | None:
        """Get material by identifier."""

        model = (
            self.session.query(MaterialModel)
            .filter(MaterialModel.id == material_id)
            .first()
        )

        if model is None:
            return None

        return self._mapper.to_domain(model)

    def get_all(
        self,
    ) -> list[DomainMaterial]:
        """Get all materials."""

        models = self.session.query(MaterialModel).all()

        return [self._mapper.to_domain(model) for model in models]

    def save(
        self,
        material: DomainMaterial,
    ) -> DomainMaterial:
        """Save material."""

        model = (
            self.session.query(MaterialModel)
            .filter(MaterialModel.id == material.id)
            .first()
        )

        if model is None:
            model = MaterialModel(
                id=material.id,
            )

            self.session.add(model)

        self._mapper.to_model(
            material,
            model,
        )

        self.session.flush()

        return material
