"""Repository dependency providers."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies.database import get_session
from app.domains.audit.repositories.audit_read_repository import AuditReadRepository
from app.domains.auth.repositories.session_repository import SessionRepository
from app.domains.customer.repositories.customer_repository import CustomerRepository
from app.domains.device.repositories.device_repository import DeviceRepository
from app.domains.diagnostic.repositories.diagnostic_repository import DiagnosticRepository
from app.domains.instrument_type.repositories.instrument_type_repository import (
    InstrumentTypeRepository,
)
from app.domains.material.repositories.material_repository import MaterialRepository
from app.domains.order.repositories.order_read_repository import OrderReadRepository
from app.domains.order.repositories.order_repository import OrderRepository
from app.domains.organization.repositories.organization_repository import (
    OrganizationRepository,
)
from app.domains.price_list.repositories.price_list_repository import PriceListRepository
from app.domains.repair.repositories.repair_repository import RepairRepository
from app.domains.site.repositories.site_repository import SiteRepository
from app.domains.user.repositories.user_repository import UserRepository
from app.domains.verification.repositories.verification_read_repository import (
    VerificationReadRepository,
)
from app.domains.verification.repositories.verification_repository import (
    VerificationRepository,
)
from app.domains.warehouse.repositories.warehouse_movement_repository import (
    WarehouseMovementRepository,
)
from app.domains.warehouse.repositories.warehouse_repository import WarehouseRepository
from app.domains.warehouse.repositories.warehouse_stock_read_repository import (
    WarehouseStockReadRepository,
)
from app.domains.warehouse.repositories.warehouse_stock_repository import (
    WarehouseStockRepository,
)
from app.domains.workflow.repositories.workflow_repository import (
    WorkflowInstanceRepository,
    WorkflowRepository,
)
from app.infrastructure.audit.audit_operation_repository import (
    AuditOperationRepositorySQLAlchemy,
)
from app.infrastructure.audit.audit_read_repository import AuditReadRepositorySQLAlchemy
from app.infrastructure.audit.audit_repository import AuditRepositorySQLAlchemy
from app.infrastructure.auth.session_repository import SessionRepositorySQLAlchemy
from app.infrastructure.customer.customer_repository import CustomerRepositorySQLAlchemy
from app.infrastructure.device.device_repository import DeviceRepositorySQLAlchemy
from app.infrastructure.diagnostic.diagnostic_repository import (
    DiagnosticRepositorySQLAlchemy,
)
from app.infrastructure.integration.integration_log_repository import (
    IntegrationLogRepositorySQLAlchemy,
)
from app.infrastructure.instrument_type.instrument_type_repository import (
    InstrumentTypeRepositorySQLAlchemy,
)
from app.infrastructure.material.material_repository import MaterialRepositorySQLAlchemy
from app.infrastructure.order.order_read_repository import OrderReadRepositorySQLAlchemy
from app.infrastructure.order.order_repository import OrderRepositorySQLAlchemy
from app.infrastructure.organization.organization_repository import (
    OrganizationRepositorySQLAlchemy,
)
from app.infrastructure.price_list.price_list_repository import PriceListRepositorySQLAlchemy
from app.infrastructure.repair.repair_repository import RepairRepositorySQLAlchemy
from app.infrastructure.site.site_repository import SiteRepositorySQLAlchemy
from app.infrastructure.user.user_repository import UserRepositorySQLAlchemy
from app.infrastructure.verification.verification_read_repository import (
    VerificationReadRepositorySQLAlchemy,
)
from app.infrastructure.verification.verification_repository import (
    VerificationRepositorySQLAlchemy,
)
from app.infrastructure.warehouse.warehouse_movement_repository import (
    WarehouseMovementRepositorySQLAlchemy,
)
from app.infrastructure.warehouse.warehouse_repository import WarehouseRepositorySQLAlchemy
from app.infrastructure.warehouse.warehouse_stock_read_repository import (
    WarehouseStockReadRepositorySQLAlchemy,
)
from app.infrastructure.warehouse.warehouse_stock_repository import (
    WarehouseStockRepositorySQLAlchemy,
)
from app.infrastructure.workflow.workflow_instance_repository import (
    WorkflowInstanceRepositorySQLAlchemy,
)
from app.infrastructure.workflow.workflow_repository import WorkflowRepositorySQLAlchemy
from app.shared.audit.repositories.audit_operation_repository import (
    AuditOperationRepository,
)
from app.shared.audit.repositories.audit_repository import AuditRepository
from app.shared.integration.repositories.integration_log_repository import (
    IntegrationLogRepository,
)


def get_integration_log_repository(
    session: Session = Depends(get_session),
) -> IntegrationLogRepository:
    """Provide IntegrationLog repository."""

    return IntegrationLogRepositorySQLAlchemy(session)


