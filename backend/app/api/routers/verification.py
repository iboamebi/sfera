"""
Verification API router.
"""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.verification.commands.approve_verification import (
    ApproveVerificationCommand,
    ApproveVerificationHandler,
)
from app.application.verification.commands.reject_verification import (
    RejectVerificationCommand,
    RejectVerificationHandler,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.core.dependencies.services import get_verification_service
from app.schemas.verification import VerificationRead

router = APIRouter(
    prefix="/verifications",
    tags=["Verifications"],
)


@router.get(
    "/{verification_id}",
    response_model=VerificationRead,
)
def get_verification(
    verification_id: UUID,
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    try:
        return service.get(verification_id)

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Verification not found",
        ) from None


@router.post(
    "/{verification_id}/approve",
    response_model=VerificationRead,
)
def approve_verification(
    verification_id: UUID,
    valid_until: date,
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    return ApproveVerificationHandler(
        service,
    ).handle(
        ApproveVerificationCommand(
            verification_id=verification_id,
            valid_until=valid_until,
        )
    )


@router.post(
    "/{verification_id}/reject",
    response_model=VerificationRead,
)
def reject_verification(
    verification_id: UUID,
    reason: str,
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    return RejectVerificationHandler(
        service,
    ).handle(
        RejectVerificationCommand(
            verification_id=verification_id,
            reason=reason,
        )
    )
