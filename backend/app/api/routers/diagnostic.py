from app.api.base_router import BaseRouter
from app.crud.diagnostic import diagnostic_crud
from app.schemas.diagnostic import (
    DiagnosticCreate,
    DiagnosticRead,
    DiagnosticUpdate,
)

router = BaseRouter(
    crud=diagnostic_crud,
    read_schema=DiagnosticRead,
    create_schema=DiagnosticCreate,
    update_schema=DiagnosticUpdate,
    prefix="/diagnostics",
    tags=["Diagnostics"],
).router
