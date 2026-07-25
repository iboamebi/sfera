"""
Application service dependency providers.
"""

from fastapi import Depends

from app.application.customer.services.customer_application_service import (
    CustomerApplicationService,
)
from app.application.device.services.device_application_service import (
    DeviceApplicationService,
)
from app.application.order.services.order_service import OrderService
from app.application.organization.services.organization_application_service import (
    OrganizationApplicationService,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.core.dependencies.repositories import (
    get_customer_repository,
    get_device_repository,
    get_order_repository,
    get_organization_repository,
    get_verification_repository,
)
from app.core.dependencies.uow import get_unit_of_work
from app.domains.customer.repositories.customer_repository import (
    CustomerRepository,
)
from app.domains.device.repositories.device_repository import (
    DeviceRepository,
)
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


def get_device_service(
    repository: DeviceRepository = Depends(get_device_repository),
) -> DeviceApplicationService:
    """Provide Device application service."""

    return DeviceApplicationService(
        repository,
    )


def get_customer_service(
    repository: CustomerRepository = Depends(get_customer_repository),
) -> CustomerApplicationService:
    """Provide Customer application service."""

    return CustomerApplicationService(
        repository,
    )


def get_organization_service(
    repository=Depends(get_organization_repository),
) -> OrganizationApplicationService:
    """Provide Organization application service."""

    return OrganizationApplicationService(
        repository,
    )
