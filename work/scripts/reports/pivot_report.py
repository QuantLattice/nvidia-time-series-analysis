"""
Pivot table report for grouped aggregation of stock data.

Groups the dataset by a specified column (default: source) and computes
configurable aggregate statistics (mean, std, min, max) for selected
numeric columns.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

from work.scripts.contracts.schemas.stock_quote_schema import StockQuoteSchema as S


@dataclass(frozen=True)
class PivotReportConfig:
    """
    Configuration for pivot table report generation.

    Attributes
    ----------
    group_column : str
        Column used for grouping rows.

    value_columns : List[str]
        Numeric columns included in aggregation.

    agg_functions : List[str]
        Pandas-compatible aggregation functions applied to each value column.
    """

    group_column: str = S.SOURCE
    value_columns: List[str] = field(
        default_factory=lambda: [
            S.OPEN_PRICE,
            S.HIGH_PRICE,
            S.LOW_PRICE,
            S.CLOSE_PRICE,
            S.VOLUME,
        ]
    )
    agg_functions: List[str] = field(
        default_factory=lambda: ["mean", "std", "min", "max", "count"]
    )


@dataclass(frozen=True)
class PivotReportResult:
    """
    Result of a pivot table aggregation.

    Attributes
    ----------
    table : pd.DataFrame
        Aggregated pivot table with multi-level column headers
        (value_column, agg_function).

    group_column : str
        Column used for row grouping.

    value_columns : List[str]
        Columns that were aggregated.

    agg_functions : List[str]
        Aggregation functions that were applied.
    """

    table: pd.DataFrame
    group_column: str
    value_columns: List[str]
    agg_functions: List[str]


class PivotReport:
    """
    Generates a pivot table by grouping data and computing aggregate statistics.

    The result is a multi-level column DataFrame indexed by group_column.
    Columns that are absent from the input are silently ignored.
    """

    def generate(
        self,
        df: pd.DataFrame,
        config: Optional[PivotReportConfig] = None,
    ) -> PivotReportResult:
        """
        Generate a pivot table report.

        Parameters
        ----------
        df : pd.DataFrame
            Input stock dataset.

        config : Optional[PivotReportConfig]
            Pivot configuration. Uses stock-data defaults when None.

        Returns
        -------
        PivotReportResult
            Grouped aggregation result.

        Raises
        ------
        ValueError
            If the group column is absent from the DataFrame.
        """

        cfg = config or PivotReportConfig()

        if cfg.group_column not in df.columns:
            raise ValueError(
                f"Group column '{cfg.group_column}' not found in DataFrame. "
                f"Available columns: {list(df.columns)}"
            )

        available_cols = [c for c in cfg.value_columns if c in df.columns]

        table = (
            df.groupby(cfg.group_column)[available_cols]
            .agg(cfg.agg_functions)
            .round(4)
        )

        return PivotReportResult(
            table=table,
            group_column=cfg.group_column,
            value_columns=available_cols,
            agg_functions=cfg.agg_functions,
        )
