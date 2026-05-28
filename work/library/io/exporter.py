"""
Multi-format export utilities for tabular data and matplotlib figures.

Supports:
- CSV export for pandas DataFrames;
- PNG export for matplotlib figures;
- PDF export for one or more matplotlib figures.

All methods create missing parent directories automatically.
"""

import os
from typing import Union

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages


class Exporter:
    """
    Exports DataFrames and matplotlib figures to CSV, PNG, or PDF.

    All methods are static and stateless; no instantiation required
    beyond Python's class syntax.
    """

    @staticmethod
    def export_csv(
        df: pd.DataFrame,
        path: str,
        index: bool = True,
        encoding: str = "utf-8-sig",
    ) -> None:
        """
        Export a DataFrame to a CSV file.

        Parameters
        ----------
        df : pd.DataFrame
            Data to export.

        path : str
            Destination file path (absolute or relative).

        index : bool, default=True
            Whether to write the DataFrame index as a column.

        encoding : str, default='utf-8-sig'
            File encoding. ``utf-8-sig`` adds a BOM for Excel compatibility.
        """

        Exporter._ensure_dir(path)
        df.to_csv(path, index=index, encoding=encoding)

    @staticmethod
    def export_png(
        figure: Figure,
        path: str,
        dpi: int = 150,
    ) -> None:
        """
        Export a matplotlib figure to a PNG file.

        Parameters
        ----------
        figure : Figure
            Matplotlib figure to save.

        path : str
            Destination file path.

        dpi : int, default=150
            Image resolution in dots per inch.
        """

        Exporter._ensure_dir(path)
        figure.savefig(path, format="png", dpi=dpi, bbox_inches="tight")

    @staticmethod
    def export_pdf(
        figures: Union[Figure, list],
        path: str,
        dpi: int = 150,
    ) -> None:
        """
        Export one or more matplotlib figures to a single multi-page PDF.

        Parameters
        ----------
        figures : Figure | list[Figure]
            Single figure or ordered list of figures to include.

        path : str
            Destination file path.

        dpi : int, default=150
            Image resolution in dots per inch.
        """

        Exporter._ensure_dir(path)

        if isinstance(figures, Figure):
            figures = [figures]

        with PdfPages(path) as pdf:
            for fig in figures:
                pdf.savefig(fig, dpi=dpi, bbox_inches="tight")

    # --------------------------------
    # PRIVATE
    # --------------------------------

    @staticmethod
    def _ensure_dir(path: str) -> None:
        parent = os.path.dirname(os.path.abspath(path))
        os.makedirs(parent, exist_ok=True)
