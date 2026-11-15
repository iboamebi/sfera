"""
Verification read service.
"""

from app.application.verification.queries.verification_read_mapper import (
    VerificationReadMapper,
)
from app.domains.verification.repositories.verification_read_repository import (
    VerificationReadRepository,
)
from app.schemas.verification import VerificationListRead


class VerificationReadService:
    """Provides read operations for the general Verification list."""

    def __init__(
        self,
        repository: VerificationReadRepository,
    ) -> None:
        self._repository = repository
        self._mapper = VerificationReadMapper()

    def list(self) -> list[VerificationListRead]:
        """List verifications using the read model."""
        return [self._mapper.to_schema(model) for model in self._repository.list()]
