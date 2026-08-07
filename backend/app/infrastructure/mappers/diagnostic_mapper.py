"""
Diagnostic mapper.
"""

from app.domains.diagnostic.entities.diagnostic import (
    Diagnostic,
)
from app.domains.diagnostic.value_objects.recommendation import (
    Recommendation,
)
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.diagnostic import Diagnostic as DiagnosticModel
from app.models.diagnostic import Recommendation as RecommendationModel


class DiagnosticMapper(
    BaseMapper[
        Diagnostic,
        DiagnosticModel,
    ],
):
    """Maps diagnostic between domain and persistence."""

    def to_domain(
        self,
        model: DiagnosticModel,
    ) -> Diagnostic:
        """Convert ORM model to domain entity."""

        return Diagnostic(
            id=model.id,
            order_item_id=model.order_item_id,
            conclusion=model.conclusion,
            recommendation=(
                Recommendation(model.recommendation.value)
                if model.recommendation
                else None
            ),
        )

    def to_model(
        self,
        entity: Diagnostic,
        model: DiagnosticModel,
    ) -> DiagnosticModel:
        """Convert domain entity to ORM model."""

        model.order_item_id = entity.order_item_id
        model.conclusion = entity.conclusion
        model.recommendation = (
            RecommendationModel(entity.recommendation.value)
            if entity.recommendation
            else None
        )

        return model
