"""
Workflow API router.
"""

from fastapi import APIRouter, Depends

from app.application.workflow.services.workflow_application_service import (
    WorkflowApplicationService,
)
from app.core.dependencies.services import get_workflow_service
from app.domains.workflow.entities.workflow import Workflow
from app.domains.workflow.entities.workflow_instance import (
    WorkflowInstance,
)

router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"],
)


@router.post("/start")
def start_workflow(
    instance: WorkflowInstance,
    service: WorkflowApplicationService = Depends(
        get_workflow_service,
    ),
):
    result = service.start(instance)

    return {
        "id": result.id,
        "status": result.status,
    }


@router.post("/move-next")
def move_workflow_stage(
    instance: WorkflowInstance,
    workflow: Workflow,
    service: WorkflowApplicationService = Depends(
        get_workflow_service,
    ),
):
    result = service.move_next(
        instance,
        workflow,
    )

    return {
        "id": result.id,
        "current_stage": result.current_stage,
        "status": result.status,
    }


@router.post("/complete")
def complete_workflow(
    instance: WorkflowInstance,
    service: WorkflowApplicationService = Depends(
        get_workflow_service,
    ),
):
    result = service.complete(instance)

    return {
        "id": result.id,
        "status": result.status,
    }
