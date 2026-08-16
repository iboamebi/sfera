"""
Infrastructure tests: InstrumentType repository.
"""

from app.infrastructure.instrument_type.instrument_type_repository import (
    InstrumentTypeRepositorySQLAlchemy,
)


def test_instrument_type_repository_class_exists():
    assert InstrumentTypeRepositorySQLAlchemy is not None
