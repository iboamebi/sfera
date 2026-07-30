"""
Repository dependency providers.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies.database import get_session
from app.infrastructure.customer.customer_repository import (
    CustomerRepositorySQLAlchemy,
)
from app.infrastructure.device.device_repository import (
    DeviceRepositorySQLAlchemy,
)
from app.infrastructure.diagnostic.diagnostic_repository import (
    DiagnosticRepositorySQLAlchemy,
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


def get_material_repository(
    session: Session = Depends(get_session),
) -> MaterialRepositorySQLAlchemy:
    """Provide Material repository."""

    return MaterialRepositorySQLAlchemy(session)


def get_diagnostic_repository(
    session: Session = Depends(get_session),
) -> DiagnosticRepositorySQLAlchemy:
    """Provide Diagnostic repository."""

    return DiagnosticRepositorySQLAlchemy(session)


def get_warehouse_repository(
    session: Session = Depends(get_session),
) -> WarehouseRepositorySQLAlchemy:
    """Provide Warehouse repository."""

    return WarehouseRepositorySQLAlchemy(session)


def get_warehouse_stock_repository(
    session: Session = Depends(get_session),
) -> WarehouseStockRepositorySQLAlchemy:
    """Provide WarehouseStock repository."""

    return WarehouseStockRepositorySQLAlchemy(session)


def get_warehouse_movement_repository(
    session: Session = Depends(get_session),
) -> WarehouseMovementRepositorySQLAlchemy:
    """Provide WarehouseMovement repository."""

    return WarehouseMovementRepositorySQLAlchemy(session)


def get_organization_repository(
    session: Session = Depends(get_session),
) -> OrganizationRepositorySQLAlchemy:
    """Provide Organization repository."""

    return OrganizationRepositorySQLAlchemy(session)


def get_customer_repository(
    session: Session = Depends(get_session),
) -> CustomerRepositorySQLAlchemy:
    """Provide Customer repository."""

    return CustomerRepositorySQLAlchemy(session)


def get_device_repository(
    session: Session = Depends(get_session),
) -> DeviceRepositorySQLAlchemy:
    """Provide Device repository."""

    return DeviceRepositorySQLAlchemy(session)


def get_order_repository(
    session: Session = Depends(get_session),
) -> OrderRepositorySQLAlchemy:
    """Provide Order repository."""

    return OrderRepositorySQLAlchemy(session)


def get_verification_repository(
    session: Session = Depends(get_session),
) -> VerificationRepositorySQLAlchemy:
    """Provide Verification repository."""

    return VerificationRepositorySQLAlchemy(session)


def get_price_list_repository(
    session: Session = Depends(get_session),
) -> PriceListRepositorySQLAlchemy:
    """Provide PriceList repository."""

    return PriceListRepositorySQLAlchemy(session)


def get_repair_repository(
    session: Session = Depends(get_session),
) -> RepairRepositorySQLAlchemy:
    """Provide Repair repository."""

    return RepairRepositorySQLAlchemy(session)
