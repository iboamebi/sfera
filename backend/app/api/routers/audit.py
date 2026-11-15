"""Administrator-only audit journal endpoint."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies.auth import get_current_user
from app.application.audit.queries.audit_read_service import AuditReadService
from app.core.dependencies.services import get_audit_read_service
from app.domains.user.entities.user import User
from app.schemas.audit import AuditRecordPageRead

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/", response_model=AuditRecordPageRead)
def list_audit_records(
    occurred_from: datetime | None = Query(default=None),
    occurred_to: datetime | None = Query(default=None),
    actor_id: UUID | None = Query(default=None),
    actor_query: str | None = Query(default=None, min_length=1, max_length=255),
    action: str | None = Query(default=None, min_length=1, max_length=100),
    entity_type: str | None = Query(default=None, min_length=1, max_length=100),
    operation_id: UUID | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    actor: User = Depends(get_current_user),
    service: AuditReadService = Depends(get_audit_read_service),
) -> AuditRecordPageRead:
    """Return persistent audit records to administrators only."""
    if occurred_from is not None and occurred_to is not None:
        if occurred_from > occurred_to:
            raise HTTPException(
                status_code=422,
                detail="occurred_from must not be later than occurred_to",
            )

    return service.list(
        actor,
        occurred_from=occurred_from,
        occurred_to=occurred_to,
        actor_id=actor_id,
        actor_query=actor_query.strip() if actor_query else None,
        action=action,
        entity_type=entity_type,
        operation_id=operation_id,
        limit=limit,
        offset=offset,
    )
