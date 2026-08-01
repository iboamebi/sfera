"""
Verification API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.verification.exceptions import (
    VerificationNotFoundApplicationError,
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
        return service.get(
            verification_id,
        )

    except VerificationNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Verification not found",
        ) from None
