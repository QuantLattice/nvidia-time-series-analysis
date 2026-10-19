"""
Descriptive statistics utilities for exploratory data analysis.

This module provides reusable scalar statistics for pandas Series,
including dispersion, data quality, robust summary statistics, and
stability metrics.

The functions are intended for use in EDA pipelines, reporting
layers, and statistical validation workflows.
"""


import pandas as pd
import numpy as np

from work.scripts.analytics.statistics.central_tendency import (
    mean,
    median
)
from work.scripts.analytics.statistics.shape_statistics import (
    skewness,
    kurtosis,
    positive_ratio,
    negative_ratio,
    zero_ratio
)

__all__ = [
    "mean",
    "median",
    "skewness",
    "kurtosis",
    "positive_ratio",
    "negative_ratio",
    "zero_ratio",
    "variance",
    "std",
    "data_range",
    "min_value",
    "max_value",
    "missing_count",
    "missing_ratio",
    "trimmed_mean",
    "mad",
    "coefficient_of_variation",
]


# =========================================================
# DISPERSION
# =========================================================

def variance(series: pd.Series) -> float:
    """
    Calculate sample variance.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Sample variance of the series.
    """

    return series.var()


def std(series: pd.Series) -> float:
    """
    Calculate sample standard deviation.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Sample standard deviation of the series.
    """

    return series.std()


def data_range(series: pd.Series) -> float:
    """
    Calculate the numerical range of the series.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Difference between maximum and minimum values.
    """

    return series.max() - series.min()


def min_value(series: pd.Series) -> float:
    """
    Return the minimum value.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Minimum value of the series.
    """

    return series.min()


def max_value(series: pd.Series) -> float:
    """
    Return the maximum value.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Maximum value of the series.
    """

    return series.max()


# =========================================================
# DATA QUALITY
# =========================================================

def missing_count(series: pd.Series) -> int:
    """
    Count missing values.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    int
        Number of missing values.
    """

    return series.isna().sum()


def missing_ratio(series: pd.Series) -> float:
    """
    Calculate the proportion of missing values.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Ratio of missing values in the series.
    """

    return series.isna().mean()


# =========================================================
# ROBUST STATISTICS
# =========================================================

def trimmed_mean(
    series: pd.Series,
    trim: float
) -> float:
    """
    Calculate the trimmed mean.

    The trimmed mean is computed by removing the lower and upper
    quantile tails defined by ``trim`` and averaging the remaining
    values.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    trim : float
        Fraction to trim from both tails of the distribution.
        Expected range is ``0 <= trim < 0.5``.

    Returns
    -------
    float
        Trimmed mean value, or NaN if the trimmed sample is empty.
    """

    clean = _safe_series(series=series)
    if clean.empty:
        return np.nan

    lower = clean.quantile(q=trim)
    upper = clean.quantile(1 - trim)

    trimmed = clean[(clean >= lower) & (clean <= upper)]

    if trimmed.empty:
        return np.nan

    return trimmed.mean()


def mad(series: pd.Series) -> float:
    """
    Calculate the median absolute deviation (MAD).

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Median absolute deviation, or NaN if the series is empty.
    """

    clean = _safe_series(series=series)
    if clean.empty:
        return np.nan

    median_val = clean.median()
    return np.median(np.abs(clean - median_val))


# =========================================================
# STABILITY METRIC
# =========================================================

def coefficient_of_variation(series: pd.Series) -> float:
    """
    Calculate the coefficient of variation.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Standard deviation divided by mean, or NaN if undefined.
    """

    clean = _safe_series(series=series)
    if clean.empty:
        return np.nan

    mean_val = clean.mean()
    if mean_val == 0:
        return np.nan

    return clean.std() / mean_val


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
