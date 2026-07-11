from app.crud.base import BaseCRUD
from app.models.verification import Verification
from app.schemas.verification import (
    VerificationCreate,
    VerificationUpdate,
)


class VerificationCRUD(
    BaseCRUD[
        Verification,
        VerificationCreate,
        VerificationUpdate,
    ]
):
    pass


verification_crud = VerificationCRUD(Verification)
