"""
Additional GUI views and popup windows.

This package contains auxiliary interface components that are opened
from menus, buttons, and other interactive GUI elements.
"""


from .settings_menu import SettingsMenu
from .calendar_popup import CalendarPopup


__all__ = [
    "SettingsMenu",
    "CalendarPopup",
]
