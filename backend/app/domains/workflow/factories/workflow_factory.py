"""
Workflow factory.

Creates Workflow aggregates with validation and default state.
"""

from __future__ import annotations

from app.domains.workflow.entities.workflow import Workflow


class WorkflowFactory:
    """Factory for Workflow aggregate."""

    @staticmethod
    def create(
        *,
        code: str,
        name: str,
        description: str | None = None,
        is_active: bool = True,
    ) -> Workflow:
        """Create a new Workflow aggregate."""

        code = code.strip().upper()
        name = name.strip()

        if not code:
            raise ValueError("Workflow code cannot be empty.")

        if not name:
            raise ValueError("Workflow name cannot be empty.")

        return Workflow(
            code=code,
            name=name,
            description=description,
            is_active=is_active,
        )
