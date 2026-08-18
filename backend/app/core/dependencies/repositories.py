"""
Repository dependency providers.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies.database import get_session
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
from app.domains.order.repositories.order_repository import (
    OrderRepository,
)
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
from app.infrastructure.auth.session_repository import (
    SessionRepositorySQLAlchemy,
)
from app.infrastructure.customer.customer_repository import (
    CustomerRepositorySQLAlchemy,
)
from app.infrastructure.device.device_repository import (
    DeviceRepositorySQLAlchemy,
)
from app.infrastructure.diagnostic.diagnostic_repository import (
    DiagnosticRepositorySQLAlchemy,
)
from app.infrastructure.instrument_type.instrument_type_repository import (
    InstrumentTypeRepositorySQLAlchemy,
)
from app.infrastructure.material.material_repository import (
    MaterialRepositorySQLAlchemy,
)
from app.infrastructure.order.order_repository import (
    OrderRepositorySQLAlchemy,
)
from app.infrastructure.organization.organization_repository import (
    OrganizationRepositorySQLAlchemy,
)
from app.infrastructure.price_list.price_list_repository import (
    PriceListRepositorySQLAlchemy,
)
from app.infrastructure.repair.repair_repository import (
    RepairRepositorySQLAlchemy,
)
from app.infrastructure.user.user_repository import UserRepositorySQLAlchemy
from app.infrastructure.verification.verification_repository import (
    VerificationRepositorySQLAlchemy,
)
from app.infrastructure.warehouse.warehouse_movement_repository import (
    WarehouseMovementRepositorySQLAlchemy,
)
from app.infrastructure.warehouse.warehouse_repository import (
    WarehouseRepositorySQLAlchemy,
)
from app.infrastructure.warehouse.warehouse_stock_repository import (
    WarehouseStockRepositorySQLAlchemy,
)
from app.infrastructure.workflow.workflow_instance_repository import (
    WorkflowInstanceRepositorySQLAlchemy,
)
from app.infrastructure.workflow.workflow_repository import WorkflowRepositorySQLAlchemy


def get_material_repository(
    session: Session = Depends(get_session),
) -> MaterialRepository:
    """Provide Material repository."""

    return MaterialRepositorySQLAlchemy(session)


def get_diagnostic_repository(
    session: Session = Depends(get_session),
) -> DiagnosticRepository:
    """Provide Diagnostic repository."""

    return DiagnosticRepositorySQLAlchemy(session)


def get_warehouse_repository(
    session: Session = Depends(get_session),
) -> WarehouseRepository:
    """Provide Warehouse repository."""

    return WarehouseRepositorySQLAlchemy(session)


def get_warehouse_stock_repository(
    session: Session = Depends(get_session),
) -> WarehouseStockRepository:
    """Provide WarehouseStock repository."""

    return WarehouseStockRepositorySQLAlchemy(session)


def get_warehouse_movement_repository(
    session: Session = Depends(get_session),
) -> WarehouseMovementRepository:
    """Provide WarehouseMovement repository."""

    return WarehouseMovementRepositorySQLAlchemy(session)


def get_organization_repository(
    session: Session = Depends(get_session),
) -> OrganizationRepository:
    """Provide Organization repository."""

    return OrganizationRepositorySQLAlchemy(session)


def get_customer_repository(
    session: Session = Depends(get_session),
) -> CustomerRepository:
    """Provide Customer repository."""

    return CustomerRepositorySQLAlchemy(session)


def get_device_repository(
    session: Session = Depends(get_session),
) -> DeviceRepository:
    """Provide Device repository."""

    return DeviceRepositorySQLAlchemy(session)


def get_instrument_type_repository(
    session: Session = Depends(get_session),
) -> InstrumentTypeRepository:
    """Provide InstrumentType repository."""

    return InstrumentTypeRepositorySQLAlchemy(session)


def get_order_repository(
    session: Session = Depends(get_session),
) -> OrderRepository:
    """Provide Order repository."""

    return OrderRepositorySQLAlchemy(session)


def get_verification_repository(
    session: Session = Depends(get_session),
) -> VerificationRepository:
    """Provide Verification repository."""

    return VerificationRepositorySQLAlchemy(session)


def get_price_list_repository(
    session: Session = Depends(get_session),
) -> PriceListRepository:
    """Provide PriceList repository."""

    return PriceListRepositorySQLAlchemy(session)


def get_repair_repository(
    session: Session = Depends(get_session),
) -> RepairRepository:
    """Provide Repair repository."""

    return RepairRepositorySQLAlchemy(session)


def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    """Provide User repository."""

    return UserRepositorySQLAlchemy(session)


def get_session_repository(
    session: Session = Depends(get_session),
) -> SessionRepository:
    """Provide authenticated session repository."""

    return SessionRepositorySQLAlchemy(session)


def get_workflow_repository(
    session: Session = Depends(get_session),
) -> WorkflowRepository:
    """Provide Workflow repository."""

    return WorkflowRepositorySQLAlchemy(session)


def get_workflow_instance_repository(
    session: Session = Depends(get_session),
) -> WorkflowInstanceRepository:
    """Provide Workflow instance repository."""

    return WorkflowInstanceRepositorySQLAlchemy(session)
