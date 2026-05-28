"""
Reusable Tkinter widget factory.

This module provides centralized creation utilities for:
- themed ttk widgets;
- icon-based buttons;
- tooltip-enabled controls;
- state-bound input widgets;
- scale-aware GUI elements.

The factory ensures visual consistency across the application
by integrating configuration settings, theme tokens, UI scaling,
and widget binding services.
"""


from tkinter import ttk, Widget
from PIL.ImageTk import PhotoImage
from typing import (
    Optional,
    Union,
    Tuple,
    Dict,
    Any,
    Callable
)

from work.library.utils import ImageLoader
from work.library.config import Config

from work.scripts.gui.utils import ToolTip
from work.scripts.gui.constants import resolve_ui_scale
from work.scripts.gui.services import UIBinder
from work.scripts.gui.theme import THEMES, ThemeName


class UIFactory():
    """
    Factory for reusable themed Tkinter widgets.

    The factory centralizes widget creation logic and integrates:
    - application configuration;
    - GUI scaling;
    - theme token management;
    - image loading and caching;
    - UI state binding services.

    Parameters
    ----------
    config : Config
        Application configuration container.

    ui_binder : UIBinder
        UI state binding service.
    """

    def __init__(
        self,
        config: Config,
        ui_binder: UIBinder
    ) -> None:
        """
        Initialize GUI widget factory services.

        Parameters
        ----------
        config : Config
            Application configuration container.

        ui_binder : UIBinder
            UI state binding service.
        """

        self.config = config
        self.ui_binder = ui_binder

        self.image_loader = ImageLoader(
            base_path=self.config.app.paths.graphics_dir,
        )

        ui = self.config.user.ui

        self.set_scale(scale=ui.scale)
        self.set_theme(theme_name=ui.theme)

        self._image_cache: Dict[
            Tuple[str, str],
            PhotoImage
        ] = {}

    # =========================
    # BUTTONS
    # =========================

    def icon_button(
        self,
        parent: Widget,
        icon_path: str,
        command: Callable[[], None],
        tooltip: Optional[str] = None,
        **button_kwargs: Any,
    ) -> ttk.Button:
        """
        Create a themed icon button.

        Parameters
        ----------
        parent : Widget
            Parent Tkinter widget.

        icon_path : str
            Relative path to the icon resource.

        command : Callable[[], None]
            Callback executed when the button is pressed.

        tooltip : Optional[str], optional
            Tooltip text displayed on hover.

        **button_kwargs : Any
            Additional ttk.Button keyword arguments.

        Returns
        -------
        ttk.Button
            Configured icon button instance.
        """

        cache_key = (
            icon_path,
            str(self.scale.icon_size)
        )

        if cache_key in self._image_cache:
            image = self._image_cache[cache_key]
        else:
            image = self.image_loader.load(
                rel_path=icon_path,
            )
            image = self.image_loader.tint_image(
                image=image,
                color=self.colors.icon
            )
            image = self.image_loader.to_photo(
                image=image
            )

        self._image_cache[cache_key] = image

        button = ttk.Button(
            master=parent,
            image=image,
            command=command,
            **button_kwargs,
        )

        if tooltip is not None:
            font = (
                self.config.user.ui.font_family,
                self.scale.font_size
            )
            ToolTip(
                widget=button,
                text=tooltip,
                colors=self.colors,
                font=font,
                icon_size=self.scale.icon_size
            )

        return button

    def text_button(
        self,
        parent: Widget,
        text: str,
        command: Callable[[], None],
        **button_kwargs: Any,
    ) -> ttk.Button:
        """
        Create a standard themed text button.

        Parameters
        ----------
        parent : Widget
            Parent Tkinter widget.

        text : str
            Button display text.

        command : Callable[[], None]
            Callback executed when the button is pressed.

        **button_kwargs : Any
            Additional ttk.Button keyword arguments.

        Returns
        -------
        ttk.Button
            Configured text button instance.
        """

        return ttk.Button(
            master=parent,
            text=text,
            command=command,
            **button_kwargs,
        )

    # =========================
    # INPUTS
    # =========================

    def bound_entry(
        self,
        parent: Widget,
        section: str,
        key: str,
        **entry_kwargs: Any
    ) -> ttk.Entry:
        """
        Create an entry widget bound to application UI state.

        Parameters
        ----------
        parent : Widget
            Parent Tkinter widget.

        section : str
            Application state section name.

        key : str
            State field key.

        **entry_kwargs : Any
            Additional ttk.Entry keyword arguments.

        Returns
        -------
        ttk.Entry
            Bound entry widget instance.
        """

        entry = ttk.Entry(
            master=parent,
            **entry_kwargs
        )

        self.ui_binder.bind_entry(
            entry=entry,
            section=section,
            key=key
        )

        return entry

    def set_theme(self, theme_name: str) -> None:
        """
        Set active GUI theme tokens.

        Parameters
        ----------
        theme_name : str
            Theme identifier.
        """

        self.colors = THEMES[ThemeName(theme_name)]

    def set_scale(
        self,
        scale: str
    ) -> None:
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

    def update(self):
        """
        Refresh internal factory resources.
        """

        self._clear_cache()

    def _clear_cache(self):
        """
        Clear cached image resources.
        """

        self._image_cache.clear()
