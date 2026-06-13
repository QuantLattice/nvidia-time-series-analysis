"""
Data contracts for rolling window analysis.

This module defines structured result types returned by the
rolling analysis layer.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class RollingSeriesReport:
    """
    Rolling statistical analysis report for a single Series.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    name : str
        Resolved series name.

    window : int
        Rolling window size used for analysis.

    rolling_mean : pd.Series
        Rolling arithmetic mean.

    rolling_std : pd.Series
        Rolling standard deviation.

    rolling_min : pd.Series
        Rolling minimum values.

    rolling_max : pd.Series
        Rolling maximum values.

    rolling_zscore : pd.Series
        Rolling z-score normalization.

    rolling_volatility : pd.Series
        Rolling volatility estimate.

    rolling_momentum : pd.Series
        Rolling momentum values.

    rolling_rate_of_change : pd.Series
        Rolling rate of change values.

    rolling_variance : pd.Series
        Rolling variance values.

    rolling_cv : pd.Series
        Rolling coefficient of variation.
    """

    name: str
    window: int

    rolling_mean: pd.Series
    rolling_std: pd.Series
    rolling_min: pd.Series
    rolling_max: pd.Series
    rolling_zscore: pd.Series
    rolling_volatility: pd.Series
    rolling_momentum: pd.Series
    rolling_rate_of_change: pd.Series
    rolling_variance: pd.Series
    rolling_cv: pd.Series
