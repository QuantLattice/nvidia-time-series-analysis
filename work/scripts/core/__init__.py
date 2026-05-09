"""
Core application state module.

This package defines the runtime state container used by the GUI layer
to manage user session state, UI navigation, and shared context data.
"""


from .app_state import AppState


__all__ = [
    "AppState"
]
