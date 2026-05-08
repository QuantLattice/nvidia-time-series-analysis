"""
GUI service layer.

This package contains runtime services used by the interface:
- translation loading;
- UI settings management;
- widget binding helpers.
"""


from .translator import Translator, TranslationKeys
from .ui_binder import UIBinder
from .ui_settings import UISettings


__all__ = [
    "Translator",
    "TranslationKeys",
    "UIBinder",
    "UISettings",
]
