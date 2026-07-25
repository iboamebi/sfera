"""
Repository dependency providers.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies.database import get_session
from app.infrastructure.device.device_repository import (
    DeviceRepositorySQLAlchemy,
)
from app.infrastructure.order.order_repository import (
    OrderRepositorySQLAlchemy,
)
from app.infrastructure.verification.verification_repository import (
    VerificationRepositorySQLAlchemy,
)


def get_device_repository(
    session: Session = Depends(get_session),
) -> DeviceRepositorySQLAlchemy:
    """Provide Device repository."""

    return DeviceRepositorySQLAlchemy(session)


def get_order_repository(
    session: Session = Depends(get_session),
) -> OrderRepositorySQLAlchemy:
    """Provide Order repository."""


def get_verification_repository(
    session: Session = Depends(get_session),
) -> VerificationRepositorySQLAlchemy:
    """Provide Verification repository."""
