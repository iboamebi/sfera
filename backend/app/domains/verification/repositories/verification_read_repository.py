"""
Verification read repository interface.
"""

from abc import ABC, abstractmethod

from app.domains.verification.read_models.verification_read_models import (
    VerificationListReadData,
)


class VerificationReadRepository(ABC):
    """Read repository for the general Verification list."""

    @abstractmethod
    def list(self) -> list[VerificationListReadData]:
        """List verification read data."""
        raise NotImplementedError
