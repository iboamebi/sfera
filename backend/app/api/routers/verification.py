"""
Verification API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth import get_current_user
from app.api.security.csrf import require_csrf
from app.application.verification.commands.create_verification import (
    CreateVerificationCommand,
)
from app.application.verification.exceptions import (
    VerificationInstrumentRequiredApplicationError,
    VerificationNotFoundApplicationError,
    VerificationOrderItemNotFoundApplicationError,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.core.dependencies.services import get_verification_service
from app.domains.user.entities.user import User
from app.schemas.verification import VerificationCreate, VerificationRead

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


@router.post(
    "",
    response_model=VerificationRead,
    dependencies=[Depends(require_csrf)],
)
def create_verification(
    data: VerificationCreate,
    user: User = Depends(get_current_user),
    service: VerificationApplicationService = Depends(
        get_verification_service,
    ),
):
    try:
        return service.create(
            CreateVerificationCommand(
                order_item_id=data.order_item_id,
                verification_date=data.verification_date,
                result=data.result,
                valid_until=data.valid_until,
                unsuitable_reason=data.unsuitable_reason,
                methodology=data.methodology,
            ),
            user,
        )
    except VerificationOrderItemNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Order item not found",
        ) from None
    except VerificationInstrumentRequiredApplicationError:
        raise HTTPException(
            status_code=422,
            detail="Verification requires a concrete instrument",
        ) from None
