"""
Pairwise correlation functions for exploratory data analysis.

Provides Pearson, Spearman, and Kendall correlation coefficients
for two aligned pandas Series, plus shared result dataclasses.

Higher-level helpers (matrix construction, pair extraction, ranking)
live in correlation_pairs.py.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CorrelationMatrixResult:
    """Result container for a correlation matrix computation.

    Attributes
    ----------
    method : str
        Correlation method used to build the matrix.
    matrix : pd.DataFrame
        Correlation matrix.
    """

    method: str
    matrix: pd.DataFrame


@dataclass(frozen=True)
class CorrelationPair:
    """Pairwise correlation record.

    Attributes
    ----------
    feature_x : str
        Name of the first feature.
    feature_y : str
        Name of the second feature.
    correlation : float
        Correlation coefficient between the two features.
    """

    feature_x: str
    feature_y: str
    correlation: float


# =========================================================
# INTERNAL HELPERS
# =========================================================

def _aligned_pair(
    series_x: pd.Series,
    series_y: pd.Series,
) -> pd.DataFrame:
    """Align two series and drop missing values.

    Returns a two-column DataFrame with aligned non-NaN rows.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """
    return pd.concat(
        objs=[series_x, series_y],
        axis=1,
    ).dropna()


# =========================================================
# PAIRWISE CORRELATIONS
# =========================================================

def pearson_correlation(
    series_x: pd.Series,
    series_y: pd.Series
) -> float:
    """Calculate Pearson correlation coefficient.

    Parameters
    ----------
    series_x : pd.Series
        First input series.
    series_y : pd.Series
        Second input series.

    Returns
    -------
    float
        Pearson correlation coefficient, or NaN if no aligned
        observations are available.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """
    aligned = _aligned_pair(series_x=series_x, series_y=series_y)
    if aligned.empty:
        return np.nan
    return aligned.iloc[:, 0].corr(
        other=aligned.iloc[:, 1],
        method="pearson"
    )


def spearman_correlation(
    series_x: pd.Series,
    series_y: pd.Series
) -> float:
    """Calculate Spearman rank correlation coefficient.

    Parameters
    ----------
    series_x : pd.Series
        First input series.
    series_y : pd.Series
        Second input series.

    Returns
    -------
    float
        Spearman correlation coefficient, or NaN if no aligned
        observations are available.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """
    aligned = _aligned_pair(series_x=series_x, series_y=series_y)
    if aligned.empty:
        return np.nan
    return aligned.iloc[:, 0].corr(
        other=aligned.iloc[:, 1],
        method="spearman"
    )


def kendall_correlation(
    series_x: pd.Series,
    series_y: pd.Series
) -> float:
    """Calculate Kendall tau correlation coefficient.

    Parameters
    ----------
    series_x : pd.Series
        First input series.
    series_y : pd.Series
        Second input series.

    Returns
    -------
    float
        Kendall tau correlation coefficient, or NaN if no aligned
        observations are available.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """
    aligned = _aligned_pair(series_x=series_x, series_y=series_y)
    if aligned.empty:
        return np.nan
    return aligned.iloc[:, 0].corr(
        other=aligned.iloc[:, 1],
        method="kendall"
    )


__all__: List[str] = [
    "CorrelationMatrixResult",
    "CorrelationPair",
    "_aligned_pair",
    "pearson_correlation",
    "spearman_correlation",
    "kendall_correlation",
]
