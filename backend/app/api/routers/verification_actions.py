"""
Verification business actions.
"""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.core.dependencies.services import get_verification_service
from app.domains.user.entities.user import User

router = APIRouter(
    prefix="/verifications",
    tags=["Verifications"],
)


@router.post(
    "/{verification_id}/approve",
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def approve_verification(
    verification_id: UUID,
    valid_until: date,
    user: User = Depends(get_current_user),
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    return service.approve(
        ApproveVerificationCommand(
            verification_id=verification_id,
            valid_until=valid_until,
        ),
        user,
    )


@router.post(
    "/{verification_id}/reject",
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def reject_verification(
    verification_id: UUID,
    reason: str,
    user: User = Depends(get_current_user),
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    return service.reject(
        RejectVerificationCommand(
            verification_id=verification_id,
            reason=reason,
        ),
        user,
    )
