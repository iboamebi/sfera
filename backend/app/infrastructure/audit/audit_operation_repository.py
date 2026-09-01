"""SQLAlchemy implementation of AuditOperationRepository."""

from sqlalchemy.orm import Session

from app.models.audit_operation import AuditOperationModel
from app.shared.audit.models import AuditOperation
from app.shared.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)


class AuditOperationRepositorySQLAlchemy(AuditOperationRepository):
    """SQLAlchemy audit operation repository."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, operation: AuditOperation) -> None:
        """Persist an audit operation."""

        self.session.add(
            AuditOperationModel(
                operation_id=operation.operation_id,
                initiated_by=operation.initiated_by,
            )
        )
        self.session.flush()
