import tkinter as tk
from tkinter import ttk, Tk
from typing import Callable, Tuple

from work.library.config import Config
from work.scripts.gui.constants.scale import resolve_ui_scale
from work.scripts.gui.factories import UIFactory
from work.scripts.gui.theme import StyleName
from work.scripts.gui.services import Translator, UISettings
from work.scripts.gui.views import SettingsMenu


class MenuBar(ttk.Frame):
    def __init__(
        self,
        parent: Tk,
        config: Config,
        ui_factory: UIFactory,
        on_toggle_panels: Callable[[], None],
        on_import_csv: Callable[[], None],
        on_export_csv: Callable[[], None],
        translator: Translator,
        ui_settings: UISettings,
    ) -> None:
        super().__init__(master=parent)

        self.config = config
        self.ui_factory = ui_factory
        self.on_toggle_panels = on_toggle_panels
        self.on_import_csv = on_import_csv
        self.on_export_csv = on_export_csv
        self.translator = translator
        self.ui_settings = ui_settings

        self.settings_menu = SettingsMenu(
            parent=self,
            ui_settings=self.ui_settings,
            translator=translator,
            config=config
        )

        self._build()

    def _build(self) -> None:
        menu_bar = self.translator.get_data().menu_bar

        # ── left: File menu button ───────────────────────────────
        left = ttk.Frame(master=self)
        left.pack(side="left", fill="y")

        self.file_menu = tk.Menu(master=self, tearoff=0)
        self.file_menu.add_command(
            label=menu_bar.import_button_label,
            command=self.on_import_csv,
            font=self._get_font(),
        )
        self.file_menu.add_command(
            label=menu_bar.export_button_label,
            command=self.on_export_csv,
            font=self._get_font(),
        )

        self.file_button = self.ui_factory.text_button(
            parent=left,
            text=menu_bar.file_button_text,
            command=self._post_file_menu,
            style=StyleName.FLAT_BUTTON,
        )
        self.file_button.pack(side="left", fill="y")

        # ── right: settings + display icons ─────────────────────
        right = ttk.Frame(master=self)
        right.pack(side="right")

        assets = self.config.app.assets

        self.settings_button = self.ui_factory.icon_button(
            parent=right,
            icon_path=assets.settings_icon,
            command=self._toggle_settings_menu,
            tooltip=menu_bar.settings_button_tooltip,
        )
        self.settings_button.pack(side="right")

        self.ui_factory.icon_button(
            parent=right,
            icon_path=assets.display_icon,
            command=self.on_toggle_panels,
            tooltip=menu_bar.display_button_tooltip,
        ).pack(side="right")

    def _post_file_menu(self) -> None:
        x = self.file_button.winfo_rootx()
        y = self.file_button.winfo_rooty() + self.file_button.winfo_height()
        self.file_menu.tk_popup(x, y)

    def _toggle_settings_menu(self) -> None:
        self.settings_menu.post_under(self.settings_button)

    def _get_font(self) -> Tuple[str, int]:
        ui = self.config.user.ui
        scale = resolve_ui_scale(ui.scale)
        return (ui.font_family, scale.font_size)
