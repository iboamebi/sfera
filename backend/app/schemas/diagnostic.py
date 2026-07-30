"""
Diagnostic API schemas.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domains.diagnostic.value_objects.recommendation import (
    Recommendation,
)


class DiagnosticCreate(BaseModel):
    """Create diagnostic request."""

    order_item_id: UUID


class DiagnosticConclusion(BaseModel):
    """Update diagnostic conclusion request."""

    conclusion: str


class DiagnosticRecommendation(BaseModel):
    """Set diagnostic recommendation request."""

    recommendation: Recommendation


class DiagnosticRead(BaseModel):
    """Diagnostic response."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    order_item_id: UUID
    conclusion: str | None = None
    recommendation: Recommendation | None = None
