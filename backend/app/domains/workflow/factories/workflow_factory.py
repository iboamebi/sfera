"""
Workflow factory.
"""

from uuid import uuid4

from app.domains.workflow.entities.workflow import Workflow
from app.domains.workflow.entities.workflow_stage import WorkflowStage


class WorkflowFactory:
    """Creates standard workflows."""

    @staticmethod
    def verification_workflow() -> Workflow:
        """Create verification workflow."""

        workflow = Workflow(
            id=uuid4(),
            name="Verification workflow",
            code="VERIFICATION",
            description="Workflow for measuring instrument verification",
        )

        workflow.add_stage(
            WorkflowStage(
                id=uuid4(),
                workflow_id=workflow.id,
                order=1,
                code="RECEIVED",
                name="Received",
                performer_role="MASTER",
            )
        )

        workflow.add_stage(
            WorkflowStage(
                id=uuid4(),
                workflow_id=workflow.id,
                order=2,
                code="DIAGNOSTIC",
                name="Diagnostic",
                performer_role="MASTER",
            )
        )

        workflow.add_stage(
            WorkflowStage(
                id=uuid4(),
                workflow_id=workflow.id,
                order=3,
                code="VERIFICATION",
                name="Verification",
                performer_role="METROLOGIST",
            )
        )

        workflow.add_stage(
            WorkflowStage(
                id=uuid4(),
                workflow_id=workflow.id,
                order=4,
                code="ISSUED",
                name="Issued",
                performer_role="MANAGER",
            )
        )

        return workflow
