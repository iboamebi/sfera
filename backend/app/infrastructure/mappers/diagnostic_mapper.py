"""
Diagnostic mapper.
"""

from app.domains.diagnostic.entities.diagnostic import (
    Diagnostic,
)
from app.domains.diagnostic.value_objects.recommendation import (
    Recommendation,
)
from app.models.diagnostic import Diagnostic as DiagnosticModel


class DiagnosticMapper:
    """Maps diagnostic between domain and persistence."""

    @staticmethod
    def to_domain(
        model: DiagnosticModel,
    ) -> Diagnostic:
        """Convert model to domain entity."""

        return Diagnostic(
            id=model.id,
            order_item_id=model.order_item_id,
            conclusion=model.conclusion,
            recommendation=(
                Recommendation(model.recommendation) if model.recommendation else None
            ),
        )

    @staticmethod
    def to_model(
        entity: Diagnostic,
    ) -> DiagnosticModel:
        """Convert domain entity to persistence model."""

        return DiagnosticModel(
            id=entity.id,
            order_item_id=entity.order_item_id,
            conclusion=entity.conclusion,
            recommendation=entity.recommendation,
        )
