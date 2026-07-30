from app.crud.base import BaseCRUD
from app.models.diagnostic import Diagnostic
from app.schemas.diagnostic import (
    DiagnosticCreate,
    DiagnosticUpdate,
)


class DiagnosticCRUD(
    BaseCRUD[
        Diagnostic,
        DiagnosticCreate,
        DiagnosticUpdate,
    ]
):
    pass


diagnostic_crud = DiagnosticCRUD(Diagnostic)
