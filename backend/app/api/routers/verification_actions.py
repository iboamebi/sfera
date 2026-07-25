"""
Verification business actions.
"""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.core.dependencies.services import get_verification_service

router = APIRouter(
    prefix="/verifications",
    tags=["Verifications"],
)


@router.post("/{verification_id}/approve")
def approve_verification(
    verification_id: UUID,
    valid_until: date,
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    return service.approve(
        verification_id,
        valid_until,
    )


@router.post("/{verification_id}/reject")
def reject_verification(
    verification_id: UUID,
    reason: str,
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    return service.reject(
        verification_id,
        reason,
    )
