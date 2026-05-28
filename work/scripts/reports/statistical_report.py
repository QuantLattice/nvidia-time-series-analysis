"""
Comprehensive statistical summary report for stock price data.

Produces a structured pandas DataFrame where each row is a numeric
column and each column is a statistical metric covering central tendency,
dispersion, shape, quantiles, and data quality.
"""

from dataclasses import dataclass
from typing import List
import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis  # type: ignore


@dataclass(frozen=True)
class StatisticalReportResult:
    """
    Tabular statistical summary for all numeric dataset columns.

    Attributes
    ----------
    table : pd.DataFrame
        Rows = analyzed series; columns = statistical metrics.

    columns : List[str]
        Names of analyzed series (index of ``table``).

    metrics : List[str]
        Names of computed metrics (columns of ``table``).
    """

    table: pd.DataFrame
    columns: List[str]
    metrics: List[str]


class StatisticalReport:
    """
    Generates a comprehensive statistical summary for numeric columns.

    Computed metrics per column
    ---------------------------
    count           Non-null observation count.
    missing         Number of missing values.
    missing_pct     Missing ratio as a percentage.
    mean            Arithmetic mean.
    median          50th percentile.
    std             Sample standard deviation.
    variance        Sample variance.
    mad             Median absolute deviation.
    min             Minimum value.
    max             Maximum value.
    range           max - min.
    q25             25th percentile.
    q75             75th percentile.
    iqr             Interquartile range (q75 - q25).
    skewness        Fisher skewness (bias-corrected).
    kurtosis        Fisher kurtosis (excess, bias-corrected).
    cv              Coefficient of variation (std / mean).
    """

    _METRICS: List[str] = [
        "count", "missing", "missing_pct",
        "mean", "median", "std", "variance", "mad",
        "min", "max", "range",
        "q25", "q75", "iqr",
        "skewness", "kurtosis", "cv",
    ]

    def generate(self, df: pd.DataFrame) -> StatisticalReportResult:
        """
        Generate a statistical summary for all numeric columns.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset.

        Returns
        -------
        StatisticalReportResult
            Structured statistical summary.
        """

        numeric = df.select_dtypes(include="number")
        records = {col: self._compute(numeric[col]) for col in numeric.columns}

        table = pd.DataFrame.from_dict(
            records,
            orient="index",
            columns=self._METRICS,
        )
        table.index.name = "column"
        table = table.round(6)

        return StatisticalReportResult(
            table=table,
            columns=list(table.index),
            metrics=self._METRICS,
        )

    # --------------------------------
    # PRIVATE
    # --------------------------------

    def _compute(self, s: pd.Series) -> List:
        n = len(s)
        missing = int(s.isna().sum())
        clean = s.dropna()
        m = len(clean)

        if clean.empty:
            nan = np.nan
            return [0, missing, 100.0, nan, nan, nan, nan, nan,
                    nan, nan, nan, nan, nan, nan, nan, nan, nan]

        q25, q75 = float(clean.quantile(0.25)), float(clean.quantile(0.75))
        mean_val = float(clean.mean())
        std_val = float(clean.std())

        return [
            m,                                                      # count
            missing,                                                # missing
            missing / n * 100,                                      # missing_pct
            mean_val,                                               # mean
            float(clean.median()),                                  # median
            std_val,                                                # std
            float(clean.var()),                                     # variance
            float(np.median(np.abs(clean - clean.median()))),       # mad
            float(clean.min()),                                     # min
            float(clean.max()),                                     # max
            float(clean.max() - clean.min()),                       # range
            q25,                                                    # q25
            q75,                                                    # q75
            q75 - q25,                                              # iqr
            float(skew(clean)) if m > 2 else np.nan,               # skewness
            float(kurtosis(clean)) if m > 3 else np.nan,           # kurtosis
            std_val / mean_val if mean_val != 0 else np.nan,       # cv
        ]
