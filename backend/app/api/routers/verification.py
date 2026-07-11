from app.api.base_router import BaseRouter
from app.crud.verification import verification_crud
from app.schemas.verification import (
    VerificationCreate,
    VerificationRead,
    VerificationUpdate,
)

router = BaseRouter(
    crud=verification_crud,
    read_schema=VerificationRead,
    create_schema=VerificationCreate,
    update_schema=VerificationUpdate,
    prefix="/verifications",
    tags=["Verifications"],
).router
