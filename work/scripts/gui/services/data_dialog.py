import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional

from work.scripts.gui.services.translator import (
    Translator
)


class DataDialogService:
    def __init__(
        self,
        root: tk.Misc,
        translator: Translator
    ) -> None:
        self.root = root
        self.translator = translator

    def ask_csv_to_import(self) -> Optional[Path]:
        import_dialog = self.translator.get_data() \
            .csv_data_dialog.import_data
        path = filedialog.askopenfilename(
            parent=self.root,
            title=import_dialog.title,
            filetypes=import_dialog.filetypes
        )

        return Path(path) if path else None

    def ask_csv_to_export(self) -> Optional[Path]:
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
        return messagebox.askyesno(
            title=title,
            message=message,
            parent=self.root
        )
