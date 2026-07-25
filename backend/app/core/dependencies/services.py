"""
Application service dependency providers.
"""

from fastapi import Depends

from app.application.order.services.order_service import OrderService
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.core.dependencies.repositories import (
    get_order_repository,
    get_verification_repository,
)
from app.core.dependencies.uow import get_unit_of_work
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


def get_order_service(
    repository: OrderRepository = Depends(get_order_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> OrderService:
    """Provide Order application service."""

    return OrderService(
        repository,
        uow,
    )


def get_verification_service(
    repository: VerificationRepository = Depends(get_verification_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> VerificationApplicationService:
    """Provide Verification application service."""

    return VerificationApplicationService(
        repository,
        uow,
    )
