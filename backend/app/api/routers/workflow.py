"""
Workflow API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.workflow.commands.complete_workflow import (
    CompleteWorkflowCommand,
)
from app.application.workflow.commands.move_workflow_stage import (
    MoveWorkflowStageCommand,
)
from app.application.workflow.commands.start_workflow import (
    StartWorkflowCommand,
)
from app.application.workflow.exceptions import (
    WorkflowInstanceNotFoundApplicationError,
    WorkflowNotFoundApplicationError,
)
from app.application.workflow.services.workflow_application_service import (
    WorkflowApplicationService,
)
from app.core.dependencies.services import get_workflow_service
from app.schemas.workflow import (
    WorkflowInstanceCreate,
    WorkflowInstanceRead,
    WorkflowMoveRequest,
)

router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"],
)


@router.post(
    "/start",
    response_model=WorkflowInstanceRead,
)
def start_workflow(
    data: WorkflowInstanceCreate,
    service: WorkflowApplicationService = Depends(
        get_workflow_service,
    ),
):
    command = StartWorkflowCommand(
        workflow_id=data.workflow_id,
        order_item_id=data.order_item_id,
    )

    return service.start(command)


@router.post(
    "/move-next",
    response_model=WorkflowInstanceRead,
)
def move_workflow_stage(
    workflow_instance_id: UUID,
    data: WorkflowMoveRequest,
    service: WorkflowApplicationService = Depends(
        get_workflow_service,
    ),
):
    command = MoveWorkflowStageCommand(
        workflow_id=data.workflow_id,
        workflow_instance_id=workflow_instance_id,
    )

    try:
        return service.move_next(command)

    except WorkflowInstanceNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Workflow instance not found",
        ) from None

    except WorkflowNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        ) from None


@router.post(
    "/complete",
    response_model=WorkflowInstanceRead,
)
def complete_workflow(
    workflow_instance_id: UUID,
    service: WorkflowApplicationService = Depends(
        get_workflow_service,
    ),
):
    command = CompleteWorkflowCommand(
        workflow_instance_id=workflow_instance_id,
    )

    try:
        return service.complete(command)

    except WorkflowInstanceNotFoundApplicationError:
        raise HTTPException(
            status_code=404,
            detail="Workflow instance not found",
        ) from None
