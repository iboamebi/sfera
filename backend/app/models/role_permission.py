import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class RolePermission(BaseModel):
    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
    )

    permission_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("permissions.id"),
        nullable=False,
    )
