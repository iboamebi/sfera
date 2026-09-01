"""
Import all models for SQLAlchemy metadata discovery.
"""

# ruff: noqa: F401

from app.models.arshin_export import ArshinExport
from app.models.audit_log import AuditLog
from app.models.audit_record import AuditRecordModel
from app.models.auth_session import AuthSession
from app.models.customer import Customer
from app.models.diagnostic import Diagnostic
from app.models.document import Document
from app.models.document_template import DocumentTemplate
from app.models.instrument import Instrument
from app.models.instrument_label import InstrumentLabel
from app.models.instrument_type import InstrumentType
from app.models.material import Material
from app.models.methodology import Methodology
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.organization import Organization
from app.models.permission import Permission
from app.models.price_list import PriceList
from app.models.price_list_item import PriceListItem
from app.models.production_movement import ProductionMovement
from app.models.repair import Repair
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.user_role import UserRole
from app.models.verification import Verification
from app.models.warehouse import Warehouse
from app.models.warehouse_movement import WarehouseMovement
from app.models.warehouse_stock import WarehouseStock
from app.models.workflow import Workflow
from app.models.workflow_instance import WorkflowInstance
from app.models.workflow_stage import WorkflowStage
