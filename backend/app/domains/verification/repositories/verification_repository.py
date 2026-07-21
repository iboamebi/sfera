from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.verification.entities.verification import (
    Verification,
)


class VerificationRepository(ABC):
    @abstractmethod
    def get(
        self,
        verification_id: UUID,
    ) -> Verification | None: ...

    @abstractmethod
    def save(
        self,
        verification: Verification,
    ) -> None: ...
