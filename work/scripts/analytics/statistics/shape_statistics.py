"""
Distribution shape and directional statistics for EDA.

This module provides skewness, kurtosis, and directional ratio
functions for pandas Series.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis as scipy_kurtosis  # type: ignore


# =========================================================
# SHAPE OF DISTRIBUTION
# =========================================================

def skewness(series: pd.Series) -> float:
    """
    Calculate sample skewness.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Skewness of the series, or NaN if the series is empty.
    """

    clean = _safe_series(series=series)
    if clean.empty:
        return np.nan
    return skew(a=clean)


def kurtosis(series: pd.Series) -> float:
    """
    Calculate sample kurtosis.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Kurtosis of the series, or NaN if the series is empty.
    """

    clean = _safe_series(series=series)
    if clean.empty:
        return np.nan
    return scipy_kurtosis(a=clean)


# =========================================================
# DIRECTIONAL STATISTICS
# =========================================================

def positive_ratio(series: pd.Series) -> float:
    """
    Calculate the ratio of positive values.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Share of values greater than zero, or NaN for empty series.
    """

    clean = _safe_series(series=series)
    if clean.empty:
        return np.nan
    return (clean > 0).mean()


def negative_ratio(series: pd.Series) -> float:
    """
    Calculate the ratio of negative values.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Share of values less than zero, or NaN for empty series.
    """

    clean = _safe_series(series=series)
    if clean.empty:
        return np.nan
    return (clean < 0).mean()


def zero_ratio(series: pd.Series) -> float:
    """
    Calculate the ratio of zero values.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Share of values equal to zero, or NaN for empty series.
    """

    clean = _safe_series(series=series)
    if clean.empty:
        return np.nan
    return (clean == 0).mean()


# ==========================================
# INTERNAL HELPERS
# ==========================================

def _safe_series(series: pd.Series) -> pd.Series:
    """
    Return a NaN-free copy of the input series.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    pd.Series
        Series with missing values removed.
    """

    return series.dropna()
