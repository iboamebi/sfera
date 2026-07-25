from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseCRUD[ModelType, CreateSchemaType, UpdateSchemaType]:
    def __init__(
        self,
        model,
        archive_field: str = "archived",
    ):
        self.model = model
        self.archive_field = archive_field

    def get(self, db: Session, obj_id):
        result = db.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalar_one_or_none()

    def get_all(self, db: Session):
        stmt = select(self.model)

        if hasattr(self.model, self.archive_field):
            stmt = stmt.where(getattr(self.model, self.archive_field).is_(False))

        result = db.execute(stmt)
        return result.scalars().all()

    def create(self, db: Session, data):
        obj = self.model(**data.model_dump())
        db.add(obj)
        db.flush()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj, data):
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        db.flush()
        db.refresh(obj)
        return obj

    def archive(self, db: Session, obj):
        if hasattr(obj, self.archive_field):
            setattr(obj, self.archive_field, True)

        db.flush()
        db.refresh(obj)
        return obj
