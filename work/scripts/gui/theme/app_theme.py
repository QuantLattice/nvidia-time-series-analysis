"""
Application ttk theme manager.

This module provides centralized GUI theme configuration
for the Tkinter interface. It applies ttk styles, manages
theme colors, configures fonts, and handles UI scaling.

The theme system supports:
- light and dark themes;
- ttk theme integration;
- centralized widget styling;
- dynamic UI scaling.
"""


from tkinter import ttk, Tk
from typing import Tuple

from work.library.config import Config
from work.scripts.gui.constants import resolve_ui_scale
from work.scripts.gui.theme import (
    THEMES,
    ThemeName,
    StyleName
)


class AppTheme:
    """
    Centralized application theme manager.

    The class applies ttk widget styles, root window colors,
    scaling configuration, and typography settings used
    throughout the GUI layer.

    Parameters
    ----------
    root : Tk
        Root Tkinter application window.

    config : Config
        Application configuration object.
    """

    def __init__(
        self,
        root: Tk,
        config: Config
    ) -> None:
        """
        Initialize the application theme manager.

        Parameters
        ----------
        root : Tk
            Root Tkinter application window.

        config : Config
            Application configuration object.
        """

        self.root = root
        self.config = config

        self.style = ttk.Style(root)

        ui = self.config.user.ui

        self.set_theme(ui.theme)
        self.set_scale(ui.scale)

        self.update()

    # --------------------------------
    # PUBLIC API
    # --------------------------------

    def set_theme(
        self,
        theme_name: str
    ) -> None:
        """
        Set active application color theme.

        Parameters
        ----------
        theme_name : str
            Theme identifier name.
        """

        self.colors = THEMES[ThemeName(theme_name)]

    def set_scale(
        self,
        scale: str
    ) -> None:
        """
        Set current UI scaling preset.

        Parameters
        ----------
        scale : str
            UI scale preset name.
        """

        self.scale = resolve_ui_scale(scale)

    def update(self) -> None:
        """
        Apply all theme and style configuration changes.
        """

        self._apply_base_theme()
        self._configure_root()
        self._configure_styles()

    # --------------------------------
    # INTERNAL
    # --------------------------------

    def _apply_base_theme(self) -> None:
        """
        Apply the underlying ttk theme.

        The preferred ttk theme is loaded from configuration.
        If unavailable, the fallback "clam" theme is used.
        """

        available = set(self.style.theme_names())

        preferred = self.config.user.ui.ttk_theme

        if preferred in available:
            self.style.theme_use(preferred)
        elif "clam" in available:
            self.style.theme_use("clam")

    def _configure_root(self) -> None:
        """
        Configure root window appearance.
        """

        self.root.configure(
            background=self.colors.background
        )

    def _font(self) -> Tuple[str, int]:
        """
        Build the default application font tuple.

        Returns
        -------
        Tuple[str, int]
            Font family and scaled font size.
        """

        ui = self.config.user.ui
        return (ui.font_family, self.scale.font_size)

    def _configure_styles(self) -> None:
        """
        Configure ttk widget styles.
        """

        font = self._font()

        self._configure_frames()
        self._configure_labels(font)
        self._configure_buttons(font)
        self._configure_entries(font)
        self._configure_separator()
        self._configure_scrollbar()

    def _configure_frames(self) -> None:
        """
        Configure ttk frame styles.
        """

        self.style.configure(
            style="TFrame",
            background=self.colors.background
        )

    def _configure_labels(
        self,
        font: Tuple[str, int]
    ) -> None:
        """
        Configure ttk label styles.

        Parameters
        ----------
        font : Tuple[str, int]
            Active application font tuple.
        """

        self.style.configure(
            style="TLabel",
            font=font,

            background=self.colors.surface,
            foreground=self.colors.text
        )

    def _configure_buttons(
        self,
        font: Tuple[str, int]
    ) -> None:
        """
        Configure ttk button styles.

        Parameters
        ----------
        font : Tuple[str, int]
            Active application font tuple.
        """

        self.style.configure(
            style="TButton",
            background=self.colors.button,
            foreground=self.colors.text,
            font=font
        )

        self.style.map(
            "TButton",
            background=[
                ("active", self.colors.button_hover),
                ("pressed", self.colors.button_pressed),
                ("disabled", self.colors.surface),
            ],
            foreground=[
                ("disabled", self.colors.button_text_disabled),
            ]
        )

        self.style.configure(
            StyleName.FLAT_BUTTON,
            background=self.colors.surface,
            borderwidth=0,
            focusthickness=0,
            padding=0,
        )

        self.style.map(
            StyleName.FLAT_BUTTON,
            background=[
                ("active", self.colors.button_hover),
                ("pressed", self.colors.button_hover),
            ],
        )

    def _configure_entries(
        self,
        font: Tuple[str, int]
    ) -> None:
        """
        Configure ttk entry styles.

        Parameters
        ----------
        font : Tuple[str, int]
            Active application font tuple.
        """

        self.style.configure(
            "TEntry",
            fieldbackground=self.colors.input_background,
            foreground=self.colors.text,

            insertcolor=self.colors.text,

            bordercolor=self.colors.border,
            focuscolor=self.colors.accent,
            font=font
        )

    def _configure_separator(self) -> None:
        """
        Configure ttk separator styles.
        """

        self.style.configure(
            style="TSeparator",
            background=self.colors.border
        )

    def _configure_scrollbar(self) -> None:
        """
        Configure ttk scrollbar styles.
        """

        self.style.configure(
            style="TScrollbar",
            background=self.colors.surface,
            troughcolor=self.colors.background,
            activebackground=self.colors.border,
        )
