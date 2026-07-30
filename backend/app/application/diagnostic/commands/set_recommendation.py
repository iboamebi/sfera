"""
Set diagnostic recommendation command.
"""

from dataclasses import dataclass
from uuid import UUID

from app.domains.diagnostic.value_objects.recommendation import (
    Recommendation,
)


@dataclass(frozen=True)
class SetRecommendationCommand:
    """Set diagnostic recommendation data."""

    diagnostic_id: UUID
    recommendation: Recommendation
