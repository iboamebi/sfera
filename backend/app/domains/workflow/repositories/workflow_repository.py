"""
Workflow repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.workflow.entities.workflow import Workflow
from app.domains.workflow.entities.workflow_instance import WorkflowInstance


class WorkflowRepository(ABC):
    """Workflow repository contract."""

    @abstractmethod
    def get(
        self,
        workflow_id: UUID,
    ) -> Workflow | None: ...

    @abstractmethod
    def save(
        self,
        workflow: Workflow,
    ) -> None: ...


class WorkflowInstanceRepository(ABC):
    """Workflow instance repository contract."""

    @abstractmethod
    def get_instance(
        self,
        instance_id: UUID,
    ) -> WorkflowInstance | None: ...

    @abstractmethod
    def save_instance(
        self,
        instance: WorkflowInstance,
    ) -> None: ...
