"""
Main application window composition.

This module builds the top-level interface, including the menu bar,
toolbar, context panel, content area, and layout orchestration.
"""


import tkinter as tk
import os

from work.scripts.core import AppState
from work.library.config import Config
from work.scripts.gui.services import UISettings, Translator
from work.scripts.gui.factories import UIFactory
from work.scripts.gui.constants import (
    MAIN_WINDOW_SIZE
)
from work.scripts.gui.layout import (
    LayoutManager,
    LayoutKey,
    LayoutRow,
    ToolBar,
    ContextPanel,
    MenuBar,
    ContentArea
)


class MainWindow:
    """
    Main application window controller.

    Parameters
    ----------
    root : tk.Tk
        Root Tkinter application window.

    config : Config
        Application configuration object.

    app_state : AppState
        Shared runtime application state.

    ui_factory : UIFactory
        Factory used to create themed UI components.

    ui_settings : UISettings
        Runtime UI configuration manager.

    translator : Translator
        Localization service used for UI text.
    """

    def __init__(
        self,
        root: tk.Tk,
        config: Config,
        app_state: AppState,
        ui_factory: UIFactory,
        ui_settings: UISettings,
        translator: Translator
    ) -> None:
        """
        Initialize and build the main application window.

        Parameters
        ----------
        root : tk.Tk
            Root Tkinter application window.

        config : Config
            Application configuration object.

        app_state : AppState
            Shared runtime application state.

        ui_factory : UIFactory
            Factory used to create themed UI components.

        ui_settings : UISettings
            Runtime UI configuration manager.

        translator : Translator
            Localization service used for UI text.
        """

        self.root = root
        self.config = config
        self.app_state = app_state
        self.ui_factory = ui_factory
        self.ui_settings = ui_settings
        self.translator = translator

        self._configure_root()
        self._build_layout()

        self.ui_settings.subscribe(callback=self.rebuild)

    # ---------------------------
    # ROOT
    # ---------------------------

    def _configure_root(self) -> None:
        """
        Configure the main Tkinter root window.
        """

        self.root.title(self.config.app.app.title)

        ui = self.config.user.ui

        self.root.geometry(
            newGeometry=(
                f"{ui.window_width}x{ui.window_height}"
                f"+{ui.window_x}+{ui.window_y}"
            )
        )

        if ui.maximized:
            self.root.after(0, lambda: self.root.state("zoomed"))

        self.root.minsize(*MAIN_WINDOW_SIZE)

        self._set_icon()

    def _set_icon(self) -> None:
        """
        Load and set the application window icon.
        """

        paths = self.config.app.paths
        assets = self.config.app.assets

        logo_path = os.path.join(paths.graphics_dir, assets.logo)
        self._logo_image = tk.PhotoImage(file=logo_path)
        self.root.iconphoto(True, self._logo_image)

    # ---------------------------
    # LAYOUT
    # ---------------------------

    def _build_layout(self) -> None:
        """
        Create all top-level GUI components and assemble the layout.
        """

        self.menu_bar = MenuBar(
            parent=self.root,
            config=self.config,
            ui_factory=self.ui_factory,
            on_toggle_panels=self.toggle_panels,
            translator=self.translator,
            ui_settings=self.ui_settings
        )

        self.toolbar = ToolBar(
            parent=self.root,
            config=self.config,
            ui_factory=self.ui_factory,
            on_click=self.on_section_click,
            translator=self.translator
        )

        self.context_panel = ContextPanel(
            parent=self.root,
            ui_factory=self.ui_factory,
            app_state=self.app_state
        )

        self.content_area = ContentArea(
            parent=self.root
        )
        self.content_area.set_placeholder(text="MAIN CONTENT")

        self.layout = LayoutManager(root=self.root)
        self.layout.register(name=LayoutKey.MENU, widget=self.menu_bar)
        self.layout.register(name=LayoutKey.TOOLBAR, widget=self.toolbar)
        self.layout.register(name=LayoutKey.CONTEXT, widget=self.context_panel)
        self.layout.register(name=LayoutKey.CONTENT, widget=self.content_area)

        self.layout.build(
            rows=[
                LayoutRow(name=LayoutKey.MENU),
                LayoutRow(name=LayoutKey.TOOLBAR),
                LayoutRow(
                    name=LayoutKey.CONTEXT,
                    visible=False
                ),
                LayoutRow(
                    name=LayoutKey.CONTENT,
                    weight=1,
                    sticky="nsew",
                    separator=False
                ),
            ]
        )

    # ---------------------------
    # LOGIC
    # ---------------------------

    def on_section_click(
        self,
        section: str
    ) -> None:
        """
        Handle toolbar section selection.

        Parameters
        ----------
        section : str
            Selected application section.
        """

        ui_state = self.app_state.ui_state

        if ui_state.active_section == section:
            ui_state.active_section = None
            self.layout.hide(name=LayoutKey.CONTEXT)
            return

        ui_state.active_section = section
        self.context_panel.render(section=section)

        self.layout.show(name=LayoutKey.CONTEXT)

    def toggle_panels(self) -> None:
        """
        Toggle visibility of toolbar and context panel.
        """

        ui_state = self.app_state.ui_state

        ui_state.panels_visible = not ui_state.panels_visible

        if ui_state.panels_visible:
            self.layout.show(name=LayoutKey.TOOLBAR)

            if ui_state.active_section is not None:
                self.context_panel.render(section=ui_state.active_section)
                self.layout.show(name=LayoutKey.CONTEXT)
            else:
                self.layout.hide(name=LayoutKey.CONTEXT)
        else:
            self.layout.hide(name=LayoutKey.TOOLBAR)
            self.layout.hide(name=LayoutKey.CONTEXT)

    def rebuild(self):
        """
        Rebuild the main window after UI settings changes.

        The current widget tree is destroyed and recreated, then the
        runtime UI state is restored.
        """

        for widget in self.root.winfo_children():
            widget.destroy()

        self._build_layout()
        self._restore_ui_state()

    def _restore_ui_state(self) -> None:
        """
        Restore layout visibility after a rebuild.
        """

        ui_state = self.app_state.ui_state

        if not ui_state.panels_visible:
            self.layout.hide(name=LayoutKey.TOOLBAR)
            self.layout.hide(name=LayoutKey.CONTEXT)
            return

        self.layout.show(name=LayoutKey.TOOLBAR)

        if ui_state.active_section is not None:
            self.context_panel.render(section=ui_state.active_section)
            self.layout.show(name=LayoutKey.CONTEXT)
        else:
            self.layout.hide(name=LayoutKey.CONTEXT)
