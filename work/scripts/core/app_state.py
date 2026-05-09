"""
Application runtime state container.

This module defines the in-memory state used by the GUI layer
during application execution. It stores UI navigation state,
contextual data between views, and session-level flags.

The state is intended to be mutable and shared across UI components,
controllers, and services.
"""


from dataclasses import dataclass, field
from typing import (
    Optional,
    Dict,
    Any
)


@dataclass
class UIState:
    """
    Mutable state of the user interface.

    Attributes
    ----------
    active_section : Optional[str]
        Currently active UI section or view identifier.

    panels_visible : bool
        Flag indicating whether side/context panels are visible.

    context_data : Dict[str, dict[str, Any]]
        Shared runtime context between UI components.
        Used for temporary view-level data exchange.
    """

    active_section: Optional[str] = None
    panels_visible: bool = True

    context_data: Dict[str, Dict[str, Any]] = field(
        default_factory=dict[str, Dict[str, Any]]
    )


class AppState():
    """
    Root application state container.

    This class acts as a single access point for all runtime UI state.
    It is intended to be injected into GUI components and services
    that require shared mutable state.

    Attributes
    ----------
    ui_state : UIState
        State object representing current GUI state.
    """

    def __init__(self) -> None:
        """
        Initialize application state with default UI state.
        """

        self.ui_state = UIState()
