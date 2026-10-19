"""
Action handler methods for the main application window.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

from datetime import date
from typing import List, Any, Optional


class MainWindowHandlersMixin:
    """
    Mixin providing action handler methods for MainWindow.

    Relies on these instance attributes provided by MainWindow.__init__:
        content_area, stock_quote_controller, data_dialog,
        _features_df, _show_report_panel

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    def _on_delete_selected(self) -> None:
        """
        Confirm and delete the currently selected table rows.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        ids = self.content_area.get_selected_ids()
        if not ids:
            self.data_dialog.show_info(
                title="Delete selected",
                message=(
                    "No rows selected. "
                    "Use Shift/Cmd+click to select rows."
                ),
            )
            return

        confirmed = self.data_dialog.ask_confirm(
            title="Delete selected",
            message=(
                f"Delete {len(ids)} selected record(s)? "
                "This cannot be undone."
            ),
        )
        if not confirmed:
            return

        errors = 0
        for quote_id in ids:
            result = self.stock_quote_controller.delete_quote_by_id(
                quote_id
            )
            if not result["success"]:
                errors += 1

        self.content_area.refresh()

        if errors:
            self.data_dialog.show_error(
                title="Delete selected",
                message=(
                    f"Deleted {len(ids) - errors} record(s). "
                    f"{errors} failed."
                ),
            )

    def _on_delete_all(self) -> None:
        """
        Confirm and delete all records from the database.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        confirmed = self.data_dialog.ask_confirm(
            title="Delete all",
            message=(
                "Delete ALL records from the database? "
                "This cannot be undone."
            ),
        )
        if not confirmed:
            return

        result = self.stock_quote_controller.delete_all_quotes()
        if result["success"]:
            deleted = result["data"]["deleted"]
            self.content_area.refresh()
            self.data_dialog.show_info(
                title="Delete all",
                message=f"Deleted {deleted} record(s).",
            )
        else:
            self.data_dialog.show_error(
                title="Delete all — Error",
                message=result["error"] or "Unknown error",
            )

    def _on_run_analysis(
        self,
        start_date: date,
        end_date: date,
        chart_type: str,
    ) -> None:
        """
        Fetch data, build the requested chart with stats, and display it.

        Parameters
        ----------
        start_date : date
            Start of the date range to analyze.
        end_date : date
            End of the date range to analyze.
        chart_type : str
            Chart type identifier (e.g. "candlestick", "line").

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        from work.scripts.gui.chart_builder import build_quote_figure
        from work.scripts.gui.stats_builder import build_stats_text

        result = self.stock_quote_controller.get_quotes_by_date_range(
            start_date=start_date,
            end_date=end_date,
        )

        if not result["success"]:
            self.content_area.set_placeholder(
                f"Error: {result['error']}"
            )
            return

        quotes: List[Any] = result["data"]

        if not quotes:
            self.content_area.set_placeholder(
                "No data found for the selected date range."
            )
            return

        fig = build_quote_figure(quotes, chart_type, start_date, end_date)
        self.content_area.show_chart(fig)

        stats_text = build_stats_text(quotes, start_date, end_date)
        self._show_report_panel(stats_text)

    def _on_generate_features(
        self,
        generator_type: str,
        start_date: date,
        end_date: date,
    ) -> Optional[List[str]]:
        """
        Fetch quotes, run the selected feature generator,
        and return numeric column names.

        Parameters
        ----------
        generator_type : str
            Name of the generator ("Moving Averages", "Returns",
            or "Technical Indicators").
        start_date : date
            Start of the date range.
        end_date : date
            End of the date range.

        Returns
        -------
        list[str] | None
            Numeric column names produced by the generator, or None on error.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        result = self.stock_quote_controller.get_quotes_by_date_range(
            start_date=start_date,
            end_date=end_date,
        )

        if not result["success"]:
            self.content_area.set_placeholder(
                f"Error: {result['error']}"
            )
            return None

        quotes: List[Any] = result["data"]

        if not quotes:
            self.content_area.set_placeholder(
                "No data found for the selected date range."
            )
            return None

        import pandas as pd
        from work.scripts.analytics.features import (
            MovingAverageFeatureGenerator,
            ReturnsFeatureGenerator,
            TechnicalIndicatorsFeatureGenerator,
        )

        df = pd.DataFrame(quotes)
        df["trade_date"] = pd.to_datetime(df["trade_date"])
        df = df.sort_values("trade_date").set_index("trade_date")

        try:
            if generator_type == "Moving Averages":
                gen = MovingAverageFeatureGenerator()
                df = gen.apply(
                    df,
                    price_column="close_price",
                    volume_column="volume"
                )
            elif generator_type == "Returns":
                gen = ReturnsFeatureGenerator()
                df = gen.apply(df, price_column="close_price")
            elif generator_type == "Technical Indicators":
                gen = TechnicalIndicatorsFeatureGenerator()
                df = gen.apply(df, price_column="close_price")
        except Exception as e:
            self.content_area.set_placeholder(
                f"Feature generation error: {e}"
            )
            return None

        self._features_df = df

        exclude = {"id"}
        return [
            c for c in df.select_dtypes(include="number").columns
            if c not in exclude
        ]

    def _on_plot_features(self, selected_columns: List[str]) -> None:
        """
        Build a multi-line chart for the selected feature columns.

        Parameters
        ----------
        selected_columns : list[str]
            Column names from the generated features DataFrame to plot.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        from work.scripts.gui.chart_builder import build_feature_figure
        from work.scripts.gui.stats_builder import build_feature_stats_text

        if self._features_df is None:
            return

        fig = build_feature_figure(self._features_df, selected_columns)
        self.content_area.show_chart(fig)

        stats_text = build_feature_stats_text(
            self._features_df, selected_columns
        )
        self._show_report_panel(stats_text)
