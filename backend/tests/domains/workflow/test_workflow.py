"""
Workflow domain tests.
"""

from app.domains.workflow.entities.workflow_instance import (
    WorkflowInstance,
)
from app.domains.workflow.factories.workflow_factory import (
    WorkflowFactory,
)
from app.domains.workflow.value_objects.workflow_status import (
    WorkflowStatus,
)


def test_create_verification_workflow():
    workflow = WorkflowFactory.verification_workflow()

    assert workflow.code == "VERIFICATION"
    assert len(workflow.stages) == 4
    assert workflow.first_stage().code == "RECEIVED"


def test_workflow_instance_start():
    workflow = WorkflowFactory.verification_workflow()

    instance = WorkflowInstance(
        workflow_id=workflow.id,
        order_item_id=workflow.id,
    )

    instance.start()

    assert instance.status == WorkflowStatus.IN_PROGRESS


def test_workflow_move_next_stage():
    workflow = WorkflowFactory.verification_workflow()

    instance = WorkflowInstance(
        workflow_id=workflow.id,
        order_item_id=workflow.id,
    )

    instance.move_next(
        last_stage=len(workflow.stages),
    )

    assert instance.current_stage == 2
