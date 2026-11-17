"""Control-panel aggregate read API."""

from fastapi import APIRouter, Depends

from app.application.control_panel.queries.control_panel_overview_service import (
    ControlPanelOverviewService,
)
from app.core.dependencies.services import get_control_panel_overview_service
from app.schemas.control_panel import ControlPanelOverviewRead

router = APIRouter(prefix="/control-panel", tags=["Control Panel"])


@router.get("/overview", response_model=ControlPanelOverviewRead)
def get_control_panel_overview(
    service: ControlPanelOverviewService = Depends(
        get_control_panel_overview_service,
    ),
) -> ControlPanelOverviewRead:
    """Return aggregate counts for the system overview."""
    return service.get_overview()
