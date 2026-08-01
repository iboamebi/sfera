"""
Diagnostic API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.diagnostic.commands.create_diagnostic import (
    CreateDiagnosticCommand,
)
from app.application.diagnostic.exceptions import (
    DiagnosticNotFoundApplicationError,
)
from app.application.diagnostic.services.diagnostic_application_service import (
    DiagnosticApplicationService,
)
from app.core.dependencies.services import get_diagnostic_service
from app.schemas.diagnostic import (
    DiagnosticConclusion,
    DiagnosticCreate,
    DiagnosticRead,
    DiagnosticRecommendation,
)

router = APIRouter(
    prefix="/diagnostics",
    tags=["Diagnostics"],
)


@router.get(
    "/{diagnostic_id}",
    response_model=DiagnosticRead,
)
def get_diagnostic(
    diagnostic_id: UUID,
    service: DiagnosticApplicationService = Depends(
        get_diagnostic_service,
    ),
):
    try:
        return service.get(
            diagnostic_id,
        )

    except DiagnosticNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Diagnostic not found",
        ) from None


@router.post(
    "",
    response_model=DiagnosticRead,
)
def create_diagnostic(
    data: DiagnosticCreate,
    service: DiagnosticApplicationService = Depends(
        get_diagnostic_service,
    ),
):
    return service.create(
        CreateDiagnosticCommand(
            order_item_id=data.order_item_id,
        ),
    )


@router.post(
    "/{diagnostic_id}/conclusion",
    response_model=DiagnosticRead,
)
def update_conclusion(
    diagnostic_id: UUID,
    data: DiagnosticConclusion,
    service: DiagnosticApplicationService = Depends(
        get_diagnostic_service,
    ),
):
    return service.update_conclusion(
        diagnostic_id,
        data.conclusion,
    )


@router.post(
    "/{diagnostic_id}/recommendation",
    response_model=DiagnosticRead,
)
def set_recommendation(
    diagnostic_id: UUID,
    data: DiagnosticRecommendation,
    service: DiagnosticApplicationService = Depends(
        get_diagnostic_service,
    ),
):
    return service.set_recommendation(
        diagnostic_id,
        data.recommendation,
    )
