"""
Verification business actions.
"""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.verification.commands.correct_verification_valid_until import (
    CorrectVerificationValidUntilCommand,
)
from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
)
from app.application.verification.commands.start_verification import (
    StartVerificationCommand,
)
from app.application.verification.exceptions import (
    VerificationCannotBeStartedApplicationError,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.core.dependencies.services import get_verification_service
from app.domains.user.entities.user import User
from app.schemas.verification import VerificationRead

router = APIRouter(
    prefix="/verifications",
    tags=["Verifications"],
)


@router.post(
    "/{verification_id}/start",
    response_model=VerificationRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def start_verification(
    verification_id: UUID,
    user: User = Depends(get_current_user),
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    try:
        return service.start(
            StartVerificationCommand(verification_id=verification_id),
            user,
        )
    except VerificationCannotBeStartedApplicationError:
        raise HTTPException(
            status_code=409,
            detail="Verification cannot be started from its current state",
        ) from None


@router.post(
    "/{verification_id}/approve",
    response_model=VerificationRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def approve_verification(
    verification_id: UUID,
    valid_until: date | None = None,
    duration_years: int | None = None,
    time_zone: str | None = None,
    user: User = Depends(get_current_user),
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    if valid_until is None and (
        duration_years is None or time_zone is None
    ):
        raise HTTPException(
            status_code=422,
            detail="Provide valid_until or duration_years and time_zone",
        )
    try:
        return service.approve(
            ApproveVerificationCommand(
                verification_id=verification_id,
                valid_until=valid_until,
                duration_years=duration_years,
                time_zone=time_zone,
            ),
            user,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from None


@router.post(
    "/{verification_id}/correct-valid-until",
    response_model=VerificationRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def correct_verification_valid_until(
    verification_id: UUID,
    valid_until: date,
    reason: str,
    user: User = Depends(get_current_user),
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    return service.correct_valid_until(
        CorrectVerificationValidUntilCommand(
            verification_id=verification_id,
            valid_until=valid_until,
            reason=reason,
        ),
        user,
    )


@router.post(
    "/{verification_id}/reject",
    response_model=VerificationRead,
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
