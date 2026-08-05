"""
Diagnostic domain entity.
"""

from dataclasses import dataclass
from uuid import UUID

from app.domains.diagnostic.value_objects.recommendation import (
    Recommendation,
)
from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class Diagnostic(Entity):
    """Represents diagnostic process."""

    order_item_id: UUID
    conclusion: str | None = None
    recommendation: Recommendation | None = None

    def complete(
        self,
        conclusion: str,
    ) -> None:
        """Complete diagnostic with conclusion."""

        self.conclusion = conclusion

    def set_recommendation(
        self,
        recommendation: Recommendation,
    ) -> None:
        """Set diagnostic recommendation."""

        self.recommendation = recommendation
