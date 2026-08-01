"""
Workflow API router.
"""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.workflow.commands.move_workflow_stage import (
    MoveWorkflowStageCommand,
)
from app.application.workflow.commands.start_workflow import (
    StartWorkflowCommand,
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

    return service.move_next(command)


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
    return service.complete(
        service.get_instance(
            workflow_instance_id,
        ),
    )
