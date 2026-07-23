"""
Workflow repository interface.

Defines persistence operations for Workflow aggregate.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.workflow.entities.workflow import Workflow


class WorkflowRepository(ABC):
    """Workflow repository interface."""

    @abstractmethod
    def add(self, workflow: Workflow) -> Workflow:
        """Create workflow."""
        raise NotImplementedError

    @abstractmethod
    def update(self, workflow: Workflow) -> Workflow:
        """Update workflow."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, workflow_id: UUID) -> None:
        """Delete workflow."""
        raise NotImplementedError

    @abstractmethod
    def get(self, workflow_id: UUID) -> Workflow | None:
        """Get workflow by id."""
        raise NotImplementedError

    @abstractmethod
    def get_by_code(self, code: str) -> Workflow | None:
        """Get workflow by code."""
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Workflow]:
        """Return all workflows."""
        raise NotImplementedError
