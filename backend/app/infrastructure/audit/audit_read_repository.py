"""SQLAlchemy implementation of the audit read repository."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, aliased

from app.domains.audit.read_models.audit_read_models import AuditRecordReadData
from app.domains.audit.repositories.audit_read_repository import AuditReadRepository
from app.models.audit_operation import AuditOperationModel
from app.models.audit_record import AuditRecordModel
from app.models.instrument import Instrument
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.repair import Repair
from app.models.user import User
from app.models.verification import Verification


class AuditReadRepositorySQLAlchemy(AuditReadRepository):
    """Read-only SQLAlchemy audit repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def list(
        self,
        *,
        occurred_from: datetime | None,
        occurred_to: datetime | None,
        actor_id: UUID | None,
        actor_query: str | None,
        action: str | None,
        entity_type: str | None,
        operation_id: UUID | None,
        limit: int,
        offset: int,
    ) -> tuple[list[AuditRecordReadData], int]:
        actor = aliased(User)
        initiator = aliased(User)
        order = aliased(Order)
        verification = aliased(Verification)
        verification_item = aliased(OrderItem)
        verification_order = aliased(Order)
        verification_instrument = aliased(Instrument)
        repair = aliased(Repair)
        repair_item = aliased(OrderItem)
        repair_order = aliased(Order)
        repair_instrument = aliased(Instrument)

        query = (
            self._session.query(
                AuditRecordModel,
                actor,
                AuditOperationModel,
                initiator,
                order,
                verification,
                verification_order,
                verification_instrument,
                repair,
                repair_order,
                repair_instrument,
            )
            .outerjoin(actor, actor.id == AuditRecordModel.actor_id)
            .outerjoin(
                AuditOperationModel,
                AuditOperationModel.operation_id == AuditRecordModel.operation_id,
            )
            .outerjoin(
                initiator,
                initiator.id == AuditOperationModel.initiated_by,
            )
            .outerjoin(
                order,
                (AuditRecordModel.entity_type == "order")
                & (order.id == AuditRecordModel.entity_id),
            )
            .outerjoin(
                verification,
                (AuditRecordModel.entity_type == "Verification")
                & (verification.id == AuditRecordModel.entity_id),
            )
            .outerjoin(
                verification_item,
                verification_item.id == verification.order_item_id,
            )
            .outerjoin(
                verification_order,
                verification_order.id == verification_item.order_id,
            )
            .outerjoin(
                verification_instrument,
                verification_instrument.id
                == func.coalesce(
                    verification.instrument_id,
                    verification_item.instrument_id,
                ),
            )
            .outerjoin(
                repair,
                (AuditRecordModel.entity_type == "repair")
                & (repair.id == AuditRecordModel.entity_id),
            )
            .outerjoin(repair_item, repair_item.id == repair.order_item_id)
            .outerjoin(repair_order, repair_order.id == repair_item.order_id)
            .outerjoin(
                repair_instrument,
                repair_instrument.id == repair_item.instrument_id,
            )
        )

        if occurred_from is not None:
            query = query.filter(AuditRecordModel.occurred_at >= occurred_from)
        if occurred_to is not None:
            query = query.filter(AuditRecordModel.occurred_at <= occurred_to)
        if actor_id is not None:
            query = query.filter(AuditRecordModel.actor_id == actor_id)
        if actor_query is not None:
            pattern = f"%{actor_query}%"
            query = query.filter(
                or_(actor.username.ilike(pattern), actor.full_name.ilike(pattern))
            )
        if action is not None:
            query = query.filter(AuditRecordModel.action == action)
        if entity_type is not None:
            query = query.filter(AuditRecordModel.entity_type == entity_type)
        if operation_id is not None:
            query = query.filter(AuditRecordModel.operation_id == operation_id)

        total = query.with_entities(func.count(AuditRecordModel.id)).scalar() or 0
        rows = (
            query.order_by(
                AuditRecordModel.occurred_at.desc(),
                AuditRecordModel.id.desc(),
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        records = []
        for (
            record,
            actor_row,
            operation,
            initiator_row,
            order_row,
            verification_row,
            verification_order_row,
            verification_instrument_row,
            repair_row,
            repair_order_row,
            repair_instrument_row,
        ) in rows:
            entity_display_name = None
            if record.entity_type == "order" and order_row is not None:
                entity_display_name = f"Заказ № {order_row.number}"
            elif record.entity_type == "Verification" and verification_row is not None:
                parts = ["Поверка"]
                if verification_order_row is not None:
                    parts.append(f"заказ № {verification_order_row.number}")
                if verification_instrument_row is not None:
                    parts.append(f"СИ № {verification_instrument_row.serial_number}")
                entity_display_name = " · ".join(parts)
            elif record.entity_type == "repair" and repair_row is not None:
                parts = ["Ремонт"]
                if repair_order_row is not None:
                    parts.append(f"заказ № {repair_order_row.number}")
                if repair_instrument_row is not None:
                    parts.append(f"СИ № {repair_instrument_row.serial_number}")
                entity_display_name = " · ".join(parts)

            records.append(
                AuditRecordReadData(
                    id=record.id,
                    operation_id=record.operation_id,
                    actor_id=record.actor_id,
                    actor_username=actor_row.username if actor_row else None,
                    actor_full_name=actor_row.full_name if actor_row else None,
                    initiated_by=operation.initiated_by if operation else None,
                    initiator_username=(
                        initiator_row.username if initiator_row else None
                    ),
                    initiator_full_name=(
                        initiator_row.full_name if initiator_row else None
                    ),
                    action=record.action,
                    entity_type=record.entity_type,
                    entity_id=record.entity_id,
                    entity_display_name=entity_display_name,
                    changes=record.changes,
                    reason=record.reason,
                    related_record_id=record.related_record_id,
                    occurred_at=record.occurred_at,
                )
            )
        return records, total
