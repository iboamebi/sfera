"""
Complete diagnostic command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CompleteDiagnosticCommand:
    """Complete diagnostic data."""

    diagnostic_id: UUID
    conclusion: str
