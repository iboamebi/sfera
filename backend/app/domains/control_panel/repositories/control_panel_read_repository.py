"""Read-only repository contract for the control-panel overview."""
from abc import ABC, abstractmethod

from app.domains.control_panel.read_models.control_panel_overview_read_model import (
    ControlPanelOverviewReadData,
)


class ControlPanelReadRepository(ABC):
    """Provides aggregate data without loading entity collections."""

    @abstractmethod
    def get_overview(self) -> ControlPanelOverviewReadData:
        """Return grouped counts from source business modules."""
        raise NotImplementedError
