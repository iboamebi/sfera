"""
Workflow application service tests.
"""

from uuid import UUID, uuid4

import pytest

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
)
from app.application.workflow.services.workflow_application_service import (
    WorkflowApplicationService,
)
from app.domains.workflow.entities.workflow import Workflow
from app.domains.workflow.entities.workflow_instance import (
    WorkflowInstance,
)
from app.domains.workflow.repositories.workflow_repository import (
    WorkflowInstanceRepository,
    WorkflowRepository,
)
from app.domains.workflow.value_objects.workflow_status import (
    WorkflowStatus,
)


class FakeWorkflowRepository(WorkflowRepository):
    def __init__(self) -> None:
        self._items: dict[UUID, Workflow] = {}

    def get(
        self,
        workflow_id: UUID,
    ) -> Workflow | None:
        return self._items.get(workflow_id)

    def save(
        self,
        workflow: Workflow,
    ) -> None:
        self._items[workflow.id] = workflow


class FakeWorkflowInstanceRepository(
    WorkflowInstanceRepository,
):
    def __init__(self) -> None:
        self._items: dict[UUID, WorkflowInstance] = {}

    def get_instance(
        self,
        instance_id: UUID,
    ) -> WorkflowInstance | None:
        return self._items.get(instance_id)

    def save_instance(
        self,
        instance: WorkflowInstance,
    ) -> None:
        self._items[instance.id] = instance


def create_workflow() -> Workflow:
    return Workflow(
        id=uuid4(),
        name="Test workflow",
        code="TEST",
    )


def test_start_workflow():
    workflow_repository = FakeWorkflowRepository()
    instance_repository = FakeWorkflowInstanceRepository()

    workflow = create_workflow()
    workflow_repository.save(workflow)

    service = WorkflowApplicationService(
        workflow_repository,
        instance_repository,
    )

    instance = service.start(
        StartWorkflowCommand(
            workflow_id=workflow.id,
            order_item_id=uuid4(),
        )
    )

    assert instance.status == WorkflowStatus.IN_PROGRESS
    assert (
        instance_repository.get_instance(
            instance.id,
        )
        == instance
    )


def test_move_workflow_next_stage():
    workflow_repository = FakeWorkflowRepository()
    instance_repository = FakeWorkflowInstanceRepository()

    workflow = create_workflow()
    workflow_repository.save(workflow)

    instance = WorkflowInstance(
        workflow_id=workflow.id,
        order_item_id=uuid4(),
    )
    instance_repository.save_instance(instance)

    service = WorkflowApplicationService(
        workflow_repository,
        instance_repository,
    )

    service.move_next(
        MoveWorkflowStageCommand(
            workflow_id=workflow.id,
            workflow_instance_id=instance.id,
        )
    )

    assert instance.current_stage == 1


def test_complete_workflow():
    workflow_repository = FakeWorkflowRepository()
    instance_repository = FakeWorkflowInstanceRepository()

    workflow = create_workflow()
    workflow_repository.save(workflow)

    instance = WorkflowInstance(
        workflow_id=workflow.id,
        order_item_id=uuid4(),
    )
    instance_repository.save_instance(instance)

    service = WorkflowApplicationService(
        workflow_repository,
        instance_repository,
    )

    service.complete(
        CompleteWorkflowCommand(
            workflow_instance_id=instance.id,
        )
    )

    assert instance.status == WorkflowStatus.COMPLETED


def test_complete_workflow_instance_not_found():
    workflow_repository = FakeWorkflowRepository()
    instance_repository = FakeWorkflowInstanceRepository()

    service = WorkflowApplicationService(
        workflow_repository,
        instance_repository,
    )

    with pytest.raises(
        WorkflowInstanceNotFoundApplicationError,
    ):
        service.complete(
            CompleteWorkflowCommand(
                workflow_instance_id=uuid4(),
            )
        )
