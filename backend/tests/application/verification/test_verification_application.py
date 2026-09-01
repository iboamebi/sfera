from datetime import date
from uuid import UUID, uuid4

import pytest

from app.application.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)
from app.application.audit.repositories.audit_repository import AuditRepository
from app.application.authorization.authorization import AuthorizationError
from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
)
from app.application.verification.exceptions import (
    VerificationNotFoundApplicationError,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.domains.verification.entities.verification import Verification
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.shared.audit.models import AuditOperation, AuditRecord
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeVerificationRepository:
    """In-memory verification repository for application tests."""

    def __init__(self, verification: Verification | None = None) -> None:
        self.verification = verification
        self.saved: list[Verification] = []

    def get(self, verification_id: UUID) -> Verification | None:
        if self.verification is not None and self.verification.id == verification_id:
            return self.verification
        return None

    def save(self, verification: Verification) -> None:
        self.saved.append(verification)


class FakeUnitOfWork:
    """In-memory unit of work for application tests."""

    def __enter__(self) -> "FakeUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None


class FakeAuditOperationRepository:
    """In-memory audit operation repository for application tests."""

    def __init__(self) -> None:
        self.saved: list[AuditOperation] = []

    def save(self, operation: AuditOperation) -> None:
        self.saved.append(operation)


class FakeAuditRepository:
    """In-memory audit repository for application tests."""

    def __init__(self) -> None:
        self.saved: list[AuditRecord] = []

    def save(self, record: AuditRecord) -> None:
        self.saved.append(record)
