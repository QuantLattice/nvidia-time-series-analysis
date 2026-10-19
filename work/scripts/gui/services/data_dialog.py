import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional

from work.scripts.gui.services.translator import (
    Translator
)


class DataDialogService:
    """
    Wrapper around Tkinter file and message dialogs.

    Parameters
    ----------
    root : tk.Misc
        Parent widget used to anchor dialog windows.
    translator : Translator
        Localization service for dialog labels.

    Авторы
    ------
    Черкащенко Данил Дмитриевич,
    Ловчиков Станислав Олегович,
    Андреева Мария Александровна
    """

    def __init__(
        self,
        root: tk.Misc,
        translator: Translator
    ) -> None:
        """
        Initialize the dialog service.

        Parameters
        ----------
        root : tk.Misc
            Parent widget used to anchor dialog windows.
        translator : Translator
            Localization service for dialog labels.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        self.root = root
        self.translator = translator

    def ask_csv_to_import(self) -> Optional[Path]:
        """
        Open a file chooser dialog for selecting a CSV file to import.

        Returns
        -------
        Path | None
            Selected file path, or None if the dialog was cancelled.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        import_dialog = self.translator.get_data() \
            .csv_data_dialog.import_data
        path = filedialog.askopenfilename(
            parent=self.root,
            title=import_dialog.title,
            filetypes=import_dialog.filetypes
        )

        return Path(path) if path else None

    def ask_csv_to_export(self) -> Optional[Path]:
        """
        Open a save-as dialog for choosing a CSV export destination.

        Returns
        -------
        Path | None
            Selected file path, or None if the dialog was cancelled.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        export_dialog = self.translator.get_data() \
            .csv_data_dialog.import_data
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title=export_dialog.title,
            defaultextension=".csv",
            filetypes=export_dialog.filetypes,
        )

        return Path(path) if path else None

    def ask_txt_to_export(self) -> Optional[Path]:
        """
        Open a save-as dialog for choosing a TXT report export destination.

        Returns
        -------
        Path | None
            Selected file path, or None if the dialog was cancelled.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export TXT Report",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )
        return Path(path) if path else None

    def show_error(
        self,
        title: str,
        message: str
    ) -> None:
        """
        Display a modal error dialog.

        Parameters
        ----------
        title : str
            Dialog window title.
        message : str
            Error message text.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        messagebox.showerror(
            title=title,
            message=message,
            parent=self.root
        )

    def show_info(
        self,
        title: str,
        message: str
    ) -> None:
        """
        Display a modal informational dialog.

        Parameters
        ----------
        title : str
            Dialog window title.
        message : str
            Informational message text.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        messagebox.showinfo(
            title=title,
            message=message,
            parent=self.root
        )

    def ask_confirm(
        self,
        title: str,
        message: str
    ) -> bool:
        """
        Display a yes/no confirmation dialog.

        Parameters
        ----------
        title : str
            Dialog window title.
        message : str
            Confirmation prompt text.

        Returns
        -------
        bool
            True if the user clicked "Yes", False otherwise.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        return messagebox.askyesno(
            title=title,
            message=message,
            parent=self.root
        )
