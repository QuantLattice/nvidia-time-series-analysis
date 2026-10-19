"""
UIFactory theme/scale state management mixin.

This module provides ``UIFactoryStateMixin``, a mixin class that
encapsulates theme, scale, and icon-size state management for the
``UIFactory``. It operates on ``self._image_cache`` and
``self.image_loader`` / ``self.scale`` / ``self.colors`` which the
concrete class provides.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from typing import Tuple, Union

from work.scripts.gui.constants import resolve_ui_scale
from work.scripts.gui.theme import THEMES, ThemeName


class UIFactoryStateMixin:
    """
    Mixin that adds theme and scale state management to UIFactory.

    The concrete class must provide ``self._image_cache``,
    ``self.image_loader``, ``self.scale``, and ``self.colors``
    before these methods are called (``__init__`` ordering).

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    def set_theme(self, theme_name: str) -> None:
        """
        Set active GUI theme tokens.

        Parameters
        ----------
        theme_name : str
            Theme identifier.
        """

        self.colors = THEMES[ThemeName(theme_name)]

    def set_scale(self, scale: str) -> None:
        """
        Set active GUI scaling configuration.

        Parameters
        ----------
        scale : str
            Scale preset identifier.
        """

        self.scale = resolve_ui_scale(scale_name=scale)
        self.set_icon_size(size=self.scale.icon_size)

    def set_icon_size(
        self,
        size: Union[int, Tuple[int, int]]
    ) -> None:
        """
        Set default image scaling size.

        Parameters
        ----------
        size : Union[int, tuple[int, int]]
            Target icon size.
        """

        self.image_loader.set_default_size(size=size)

    def update(self) -> None:
        """
        Refresh internal factory resources.
        """

        self._clear_cache()

    def _clear_cache(self) -> None:
        """
        Clear cached image resources.
        """

        self._image_cache.clear()
