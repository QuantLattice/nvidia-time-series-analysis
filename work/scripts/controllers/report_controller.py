"""
Controller for analytics report export.

Orchestrates data retrieval, report generation (EDA + TS),
text formatting, and file writing.
"""

from typing import Any, Callable, Dict

from work.scripts.services.stock_quote_service import StockQuoteService
from work.scripts.analytics.reports import EDAReport, TSReport
from work.scripts.services.report_formatter import ReportFormatter


class ReportController:
    """
    Generates and exports a plain-text analytics report.

    Parameters
    ----------
    service : StockQuoteService
        Data source used to build the analysis DataFrame.

    Авторы
    ------
    Черкащенко Данил Дмитриевич,
    Ловчиков Станислав Олегович,
    Андреева Мария Александровна
    """

    def __init__(self, service: StockQuoteService) -> None:
        """
        Initialize the report controller.

        Parameters
        ----------
        service : StockQuoteService
            Data source used to build the analysis DataFrame.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        self.service = service
        self._eda = EDAReport()
        self._ts = TSReport()
        self._formatter = ReportFormatter()

    def export_txt(self, path: str) -> Dict[str, Any]:
        """
        Generate a full EDA + TS report and write it to *path*.

        Parameters
        ----------
        path : str
            Absolute file path (e.g. ``/home/user/report.txt``).

        Returns
        -------
        dict
            ``{"success": True, "data": None, "error": None}`` on success,
            or ``{"success": False, "data": None, "error": <msg>}`` on failure.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        return self._handle(lambda: self._do_export(path))

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _do_export(self, path: str) -> None:
        """
        Build the full EDA + TS report and write it to the given path.

        Parameters
        ----------
        path : str
            Destination file path.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        df = self.service.get_all_quotes_df()

        if df.empty:
            raise ValueError("Нет данных в базе — сначала импортируйте CSV.")

        eda_result = self._eda.generate(df)
        ts_result = self._ts.generate(df)

        text = self._formatter.format(df=df, eda=eda_result, ts=ts_result)

        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def _handle(self, func: Callable[[], Any]) -> Dict[str, Any]:
        """
        Execute a callable and wrap the result in a standardized response dict.

        Parameters
        ----------
        func : Callable[[], Any]
            Function to execute.

        Returns
        -------
        dict[str, Any]
            ``{"success": True/False, "data": None, "error": str | None}``.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        try:
            func()
            return {"success": True, "data": None, "error": None}
        except (ValueError, OSError) as exc:
            return {"success": False, "data": None, "error": str(exc)}
        except Exception as exc:  # noqa: BLE001
            return {
                "success": False,
                "data": None,
                "error": f"{exc.__class__.__name__}: {exc}",
            }
