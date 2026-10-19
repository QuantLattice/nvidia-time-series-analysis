"""
Font selection popup window.

This module provides a popup window that allows the user to:
- browse available system fonts;
- filter fonts by name;
- preview selected fonts;
- apply a new interface font dynamically.
"""


import tkinter as tk
from tkinter import ttk, font
from typing import List, Optional, Tuple

from work.library.config import Config
from work.scripts.gui.services import UISettings, Translator
from work.scripts.gui.theme import ThemeName, THEMES
from work.scripts.gui.constants import (
    FONT_SELECTOR_POPUP_SIZE,
    resolve_ui_scale
)
from work.scripts.gui.views.font_selector_layout import (
    build_font_selector_widgets,
)


class FontSelectorPopup(tk.Toplevel):
    """
    Popup window for selecting the GUI font.

    Parameters
    ----------
    parent : ttk.Frame
        Parent container for the popup window.

    anchor : ttk.Button
        Widget used as the positioning anchor.

    ui_settings : UISettings
        Interface settings manager.

    current_font : str
        Currently selected font family.

    translator : Translator
        Translation service used for localized text.

    config : Config
        Application configuration object.
    """

    def __init__(
        self,
        parent: ttk.Frame,
        anchor: ttk.Button,
        ui_settings: UISettings,
        current_font: str,
        translator: Translator,
        config: Config
    ) -> None:
        """
        Initialize the font selection popup window.

        Parameters
        ----------
        parent : ttk.Frame
            Parent container for the popup window.

        anchor : ttk.Button
            Widget used as the positioning anchor for the popup.

        ui_settings : UISettings
            Interface settings manager used to apply font changes.

        current_font : str
            Currently selected font family.

        translator : Translator
            Translation service used for localized interface text.

        config : Config
            Application configuration object.
        """

        super().__init__(parent)

        self.ui_settings = ui_settings
        self.translator = translator
        self.config = config

        font_selector_popup = self.translator.get_data().font_selector_popup

        self._title = font_selector_popup.title
        self.example_text = font_selector_popup.example_text
        self.apply_text = font_selector_popup.apply_button_text

        ui = self.config.user.ui
        self.colors = THEMES[ThemeName(ui.theme)]

        self.fonts: list[str] = sorted(font.families())
        self.filtered_fonts: list[str] = self.fonts.copy()

        self.title(self._title)
        self.geometry(
            newGeometry=(
                f"{FONT_SELECTOR_POPUP_SIZE[0]}x"
                f"{FONT_SELECTOR_POPUP_SIZE[1]}"
            )
        )
        self.resizable(True, True)

        self.configure(
            bg=self.colors.background
        )

        # Make the popup modal relative to the parent window.
        self.transient(parent)  # type: ignore
        self.grab_set()

        self._build(current_font=current_font)
        self._position(widget=anchor)

    # --------------------------------
    # BUILD
    # --------------------------------

    def _build(self, current_font: str) -> None:
        """Build and initialize popup widgets."""

        self.listbox, self.preview, self.search_var = (
            build_font_selector_widgets(
                popup=self,
                fonts=self.filtered_fonts,
                current_font=current_font,
                example_text=self.example_text,
                apply_text=self.apply_text,
                on_select=self._on_select,
                on_apply=self._apply,
                on_filter=self._filter_fonts,
                colors=self.colors,
                get_font_fn=self._get_font,
            )
        )

        if current_font in self.fonts:
            self._update_preview(font_name=current_font)

    def _fill(self) -> None:
        """
        Fill the font listbox with filtered font names.
        """

        self.listbox.delete(first=0, last="end")

        for font_name in self.filtered_fonts:
            self.listbox.insert("end", font_name)

    def _filter_fonts(
        self,
        event: Optional[tk.Event] = None
    ) -> None:
        """
        Filter available fonts using the search query.

        Parameters
        ----------
        event : Optional[tk.Event], optional
            Tkinter event object.
        """

        query = self.search_var.get().lower()

        self.filtered_fonts = [
            font_name for font_name in self.fonts
            if query in font_name.lower()
        ]

        self._fill()

    def _on_select(
        self,
        event: Optional[tk.Event] = None
    ) -> None:
        """
        Handle font selection changes.

        Parameters
        ----------
        event :  Optional[tk.Event], optional
            Tkinter event object.
        """

        selection = self.listbox.curselection()  # type: ignore
        selection: List[int]

        if not selection:
            return

        font_name = self.filtered_fonts[selection[0]]
        self._update_preview(font_name=font_name)

    def _update_preview(
        self,
        font_name: str
    ) -> None:
        """
        Update the preview area using the selected font.

        Parameters
        ----------
        font_name : str
            Selected font family.
        """

        self.preview.config(state="normal")

        self.preview.delete(index1="1.0", index2="end")
        self.preview.insert(index="1.0", chars=self.example_text)

        self.preview.config(font=(font_name, self._get_font()[1]))

        self.preview.config(state="disabled")

    def _apply(
        self,
        event: Optional[tk.Event] = None
    ) -> None:
        """
        Apply the selected font to the interface.

        Parameters
        ----------
        event : Optional[tk.Event], optional
            Tkinter event object.
        """

        selection = self.listbox.curselection()  # type: ignore
        selection: List[int]

        if not selection:
            return

        font_name = self.filtered_fonts[selection[0]]

        self.ui_settings.set_font(font=font_name)

        self.destroy()

    def _position(
        self,
        widget: tk.Widget
    ) -> None:
        """
        Position the popup relative to the anchor widget.

        Parameters
        ----------
        widget : tk.Widget
            Anchor widget used for popup placement.
        """

        self.update_idletasks()
        widget.update_idletasks()

        width = FONT_SELECTOR_POPUP_SIZE[0]
        height = FONT_SELECTOR_POPUP_SIZE[1]

        x = widget.winfo_rootx()
        y = widget.winfo_rooty() + widget.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        if x + width > screen_width:
            x = screen_width - width - 10

        if y + height > screen_height:
            y = widget.winfo_rooty() - height

        self.geometry(newGeometry=f"{width}x{height}+{x}+{y}")

    # --------------------------------
    # HELPERS
    # --------------------------------

    def _get_font(self) -> Tuple[str, int]:
        """
        Build the default UI font tuple.

        Returns
        -------
        Tuple[str, int]
            Font family and scaled font size.
        """

        ui = self.config.user.ui
        scale = resolve_ui_scale(ui.scale)

        return (ui.font_family, scale.font_size)
