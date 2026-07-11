from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db


class BaseRouter:
    def __init__(
        self,
        *,
        crud,
        read_schema,
        create_schema,
        update_schema,
        prefix: str,
        tags: list[str],
    ):
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,
        )

        @self.router.get("/", response_model=list[read_schema])
        def get_all(db: Session = Depends(get_db)):
            return crud.get_all(db)

        @self.router.get("/{obj_id}", response_model=read_schema)
        def get_one(
            obj_id: UUID,
            db: Session = Depends(get_db),
        ):
            obj = crud.get(db, obj_id)
            if obj is None:
                raise HTTPException(404, "Object not found")
            return obj

        @self.router.post("/", response_model=read_schema, status_code=201)
        def create(
            data: create_schema,
            db: Session = Depends(get_db),
        ):
            return crud.create(db, data)

        @self.router.patch("/{obj_id}", response_model=read_schema)
        def update(
            obj_id: UUID,
            data: update_schema,
            db: Session = Depends(get_db),
        ):
            obj = crud.get(db, obj_id)
            if obj is None:
                raise HTTPException(404, "Object not found")

            return crud.update(db, obj, data)

        @self.router.delete("/{obj_id}", response_model=read_schema)
        def delete(
            obj_id: UUID,
            db: Session = Depends(get_db),
        ):
            obj = crud.get(db, obj_id)
            if obj is None:
                raise HTTPException(404, "Object not found")

            return crud.archive(db, obj)
