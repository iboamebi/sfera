"""
Application service dependency providers.
"""

from datetime import timedelta

from fastapi import Depends

from app.application.auth.services.authentication_application_service import (
    AuthenticationApplicationService,
)
from app.application.auth.services.session_application_service import (
    SessionApplicationService,
)
from app.application.customer.services.customer_application_service import (
    CustomerApplicationService,
)
from app.application.device.services.device_application_service import (
    DeviceApplicationService,
)
from app.application.diagnostic.services.diagnostic_application_service import (
    DiagnosticApplicationService,
)
from app.application.instrument_type.services import (
    instrument_type_application_service,
)
from app.application.material.services.material_application_service import (
    MaterialApplicationService,
)
from app.application.order.services.order_application_service import (
    OrderApplicationService,
)
from app.application.organization.services.organization_application_service import (
    OrganizationApplicationService,
)
from app.application.price_list.services.price_list_application_service import (
    PriceListApplicationService,
)
from app.application.repair.services.repair_application_service import (
    RepairApplicationService,
)
from app.application.verification.services.verification_application_service import (
    VerificationApplicationService,
)
from app.application.warehouse.services.warehouse_application_service import (
    WarehouseApplicationService,
)
from app.application.workflow.services.workflow_application_service import (
    WorkflowApplicationService,
)
from app.core.dependencies.repositories import (
    get_customer_repository,
    get_device_repository,
    get_diagnostic_repository,
    get_instrument_type_repository,
    get_material_repository,
    get_order_repository,
    get_organization_repository,
    get_price_list_repository,
    get_repair_repository,
    get_session_repository,
    get_user_repository,
    get_verification_repository,
    get_warehouse_movement_repository,
    get_warehouse_repository,
    get_warehouse_stock_repository,
    get_workflow_instance_repository,
    get_workflow_repository,
)
from app.core.dependencies.uow import get_unit_of_work
from app.domains.auth.repositories.session_repository import SessionRepository
from app.domains.customer.repositories.customer_repository import (
    CustomerRepository,
)
from app.domains.device.repositories.device_repository import (
    DeviceRepository,
)
from app.domains.diagnostic.repositories.diagnostic_repository import (
    DiagnosticRepository,
)
from app.domains.instrument_type.repositories.instrument_type_repository import (
    InstrumentTypeRepository,
)
from app.domains.material.repositories.material_repository import (
    MaterialRepository,
)
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.organization.repositories.organization_repository import (
    OrganizationRepository,
)
from app.domains.price_list.repositories.price_list_repository import (
    PriceListRepository,
)
from app.domains.repair.repositories.repair_repository import (
    RepairRepository,
)
from app.domains.user.repositories.user_repository import UserRepository
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.domains.warehouse.repositories.warehouse_movement_repository import (
    WarehouseMovementRepository,
)
from app.domains.warehouse.repositories.warehouse_repository import (
    WarehouseRepository,
)
from app.domains.warehouse.repositories.warehouse_stock_repository import (
    WarehouseStockRepository,
)
from app.domains.workflow.repositories.workflow_repository import (
    WorkflowInstanceRepository,
    WorkflowRepository,
)
from app.infrastructure.auth.password_hasher import Argon2PasswordHasher
from app.infrastructure.auth.session_token_generator import (
    SecureSessionTokenGenerator,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


def get_password_hasher() -> Argon2PasswordHasher:
    """Provide password hasher implementation."""

    return Argon2PasswordHasher()


def get_authentication_service(
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: Argon2PasswordHasher = Depends(get_password_hasher),
) -> AuthenticationApplicationService:
    """Provide Authentication application service."""

    return AuthenticationApplicationService(
        repository,
        password_hasher,
    )


def get_session_token_generator() -> SecureSessionTokenGenerator:
    """Provide secure authenticated session token generator."""

    return SecureSessionTokenGenerator()


def get_session_service(
    repository: SessionRepository = Depends(get_session_repository),
    token_generator: SecureSessionTokenGenerator = Depends(
        get_session_token_generator,
    ),
) -> SessionApplicationService:
    """Provide authenticated session application service."""

    return SessionApplicationService(
        repository,
        token_generator,
        ttl=timedelta(hours=12),
    )


def get_order_service(
    repository: OrderRepository = Depends(get_order_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> OrderApplicationService:
    """Provide Order application service."""

    return OrderApplicationService(
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
    instrument_type_repository: InstrumentTypeRepository = Depends(
        get_instrument_type_repository,
    ),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> DeviceApplicationService:
    """Provide Device application service."""

    return DeviceApplicationService(
        repository,
        instrument_type_repository,
        uow,
    )


def get_instrument_type_service(
    repository: InstrumentTypeRepository = Depends(
        get_instrument_type_repository,
    ),
) -> instrument_type_application_service.InstrumentTypeApplicationService:
    """Provide InstrumentType application service."""

    return instrument_type_application_service.InstrumentTypeApplicationService(
        repository,
    )


def get_customer_service(
    repository: CustomerRepository = Depends(get_customer_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CustomerApplicationService:
    """Provide Customer application service."""

    return CustomerApplicationService(
        repository,
        uow,
    )


def get_material_service(
    repository: MaterialRepository = Depends(get_material_repository),
) -> MaterialApplicationService:
    """Provide Material application service."""

    return MaterialApplicationService(repository)


def get_warehouse_service(
    warehouse_repository: WarehouseRepository = Depends(
        get_warehouse_repository,
    ),
    stock_repository: WarehouseStockRepository = Depends(
        get_warehouse_stock_repository,
    ),
    movement_repository: WarehouseMovementRepository = Depends(
        get_warehouse_movement_repository,
    ),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> WarehouseApplicationService:
    """Provide Warehouse application service."""

    return WarehouseApplicationService(
        warehouse_repository,
        stock_repository,
        movement_repository,
        uow,
    )


def get_organization_service(
    repository: OrganizationRepository = Depends(
        get_organization_repository,
    ),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> OrganizationApplicationService:
    """Provide Organization application service."""

    return OrganizationApplicationService(
        repository,
        uow,
    )


def get_workflow_service(
    repository: WorkflowRepository = Depends(
        get_workflow_repository,
    ),
    instance_repository: WorkflowInstanceRepository = Depends(
        get_workflow_instance_repository,
    ),
) -> WorkflowApplicationService:
    """Provide Workflow application service."""

    return WorkflowApplicationService(
        repository,
        instance_repository,
    )


def get_price_list_service(
    repository: PriceListRepository = Depends(get_price_list_repository),
) -> PriceListApplicationService:
    """Provide PriceList application service."""

    return PriceListApplicationService(repository)


def get_repair_service(
    repository: RepairRepository = Depends(get_repair_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> RepairApplicationService:
    """Provide Repair application service."""

    return RepairApplicationService(
        repository,
        uow,
    )


def get_diagnostic_service(
    repository: DiagnosticRepository = Depends(
        get_diagnostic_repository,
    ),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> DiagnosticApplicationService:
    """Provide Diagnostic application service."""

    return DiagnosticApplicationService(
        repository,
        uow,
    )
