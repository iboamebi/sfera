"""
Create material command.

Defines input data for creating a new Material.
Version: 2.0
Revision: 2026-08-11
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateMaterialCommand:
    """Command for creating a material."""

    name: str
    article: str | None
    unit: str
    description: str | None
