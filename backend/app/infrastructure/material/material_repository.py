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
from app.models.material import Material as MaterialModel


class MaterialRepositorySQLAlchemy(MaterialRepository):
    """SQLAlchemy material repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

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

        return DomainMaterial(
            id=model.id,
            name=model.name,
            article=model.article,
            unit=model.unit,
            description=model.description,
            archived=model.archived,
        )

    def get_all(
        self,
    ) -> list[DomainMaterial]:
        """Get all materials."""

        models = self.session.query(MaterialModel).all()

        return [
            DomainMaterial(
                id=model.id,
                name=model.name,
                article=model.article,
                unit=model.unit,
                description=model.description,
                archived=model.archived,
            )
            for model in models
        ]

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
                name=material.name,
                article=material.article,
                unit=material.unit,
                description=material.description,
                archived=material.archived,
            )

            self.session.add(model)

        else:
            model.name = material.name
            model.article = material.article
            model.unit = material.unit
            model.description = material.description
            model.archived = material.archived

        self.session.flush()

        return material
