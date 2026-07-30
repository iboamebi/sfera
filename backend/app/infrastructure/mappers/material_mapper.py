"""
Material mapper.
"""

from app.domains.material.entities.material import Material
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.material import Material as MaterialModel


class MaterialMapper(BaseMapper[Material, MaterialModel]):
    """Material mapper."""

    def to_domain(
        self,
        model: MaterialModel,
    ) -> Material:
        return Material(
            id=model.id,
            name=model.name,
            article=model.article,
            unit=model.unit,
            description=model.description,
            archived=model.archived,
        )

    def to_model(
        self,
        entity: Material,
        model: MaterialModel,
    ) -> MaterialModel:
        model.name = entity.name
        model.article = entity.article
        model.unit = entity.unit
        model.description = entity.description
        model.archived = entity.archived

        return model
