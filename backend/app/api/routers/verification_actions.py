"""
Verification business actions.
"""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
)
from app.application.verification.commands.correct_verification_decision import (
    CorrectVerificationDecisionCommand,
)
from app.application.verification.commands.correct_verification_valid_until import (
    CorrectVerificationValidUntilCommand,
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
from app.domains.verification.exceptions import (
    InvalidDecisionCorrectionDomainError,
    InvalidDecisionCorrectionReasonDomainError,
    InvalidUnsuitableReasonDomainError,
    InvalidVerificationResultStateDomainError,
)
from app.schemas.verification import (
    VerificationDecisionCorrection,
    VerificationRead,
)

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
    if valid_until is None and (duration_years is None or time_zone is None):
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
    if not reason.strip():
        raise HTTPException(
            status_code=422,
            detail="Correction reason is required",
        )
    try:
        return service.correct_valid_until(
            CorrectVerificationValidUntilCommand(
                verification_id=verification_id,
                valid_until=valid_until,
                reason=reason,
            ),
            user,
        )
    except InvalidVerificationResultStateDomainError:
        raise HTTPException(
            status_code=409,
            detail="Only a suitable decided verification can be corrected",
        ) from None


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


@router.post(
    "/{verification_id}/correct-decision",
    response_model=VerificationRead,
    dependencies=[Depends(get_current_user), Depends(require_csrf)],
)
def correct_verification_decision(
    verification_id: UUID,
    payload: VerificationDecisionCorrection,
    user: User = Depends(get_current_user),
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    if not payload.reason.strip():
        raise HTTPException(
            status_code=422,
            detail="Correction reason is required",
        )
    try:
        return service.correct_decision(
            CorrectVerificationDecisionCommand(
                verification_id=verification_id,
                result=payload.result,
                valid_until=payload.valid_until,
                unsuitable_reason=payload.unsuitable_reason,
                reason=payload.reason,
            ),
            user,
        )
    except InvalidVerificationResultStateDomainError:
        raise HTTPException(
            status_code=409,
            detail="Only a decided verification can be corrected",
        ) from None
    except (
        InvalidDecisionCorrectionDomainError,
        InvalidDecisionCorrectionReasonDomainError,
        InvalidUnsuitableReasonDomainError,
    ):
        raise HTTPException(
            status_code=422,
            detail="Corrected decision fields do not match the selected result",
        ) from None
