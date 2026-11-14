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
    def has_active_for_order_item(self, order_item_id: UUID) -> bool: ...

    @abstractmethod
    def save(
        self,
        verification: Verification,
    ) -> None: ...
