"""
Archive InstrumentType command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ArchiveInstrumentTypeCommand:
    """Archive instrument type command."""

    instrument_type_id: UUID
