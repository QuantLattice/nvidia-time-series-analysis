"""
Distribution statistics for exploratory data analysis.

This module provides reusable distribution-oriented statistics for
pandas Series, including quantiles, interquartile range, outlier
bounds, histogram summaries, and empirical cumulative distribution
function data.
"""


from dataclasses import dataclass
import numpy as np
import pandas as pd
from typing import List, Dict


@dataclass(frozen=True)
class OutlierBounds:
    """
    Interquartile outlier bounds.

    Attributes
    ----------
    lower : float
        Lower outlier boundary.

    upper : float
        Upper outlier boundary.
    """

    lower: float
    upper: float


@dataclass(frozen=True)
class HistogramResult:
    """
    Histogram summary result.

    Attributes
    ----------
    counts : np.ndarray
        Bin counts.

    bin_edges : np.ndarray
        Bin edge values.

    bins : int
        Number of histogram bins used.
    """

    counts: np.ndarray
    bin_edges: np.ndarray
    bins: int


@dataclass(frozen=True)
class EmpiricalCDFResult:
    """
    Empirical cumulative distribution function result.

    Attributes
    ----------
    values : np.ndarray
        Sorted sample values.

    cdf : np.ndarray
        Empirical cumulative probabilities.
    """

    values: np.ndarray
    cdf: np.ndarray


def quantiles(
    series: pd.Series,
    probs: List[float]
) -> Dict[float, float]:
    """
    Calculate requested quantiles.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    probs : List[float]
        Quantile probabilities in the range [0, 1].

    Returns
    -------
    Dict[float, float]
        Mapping of probability to quantile value.
    """

    clean = series.dropna()
    return {p: clean.quantile(p) for p in probs}


def iqr(series: pd.Series) -> float:
    """
    Calculate interquartile range.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Interquartile range, defined as Q3 - Q1.
    """

    q1 = series.quantile(q=0.25)
    q3 = series.quantile(q=0.75)
    return q3 - q1


def outlier_bounds(
    series: pd.Series,
    k: float
) -> OutlierBounds:
    """
    Calculate Tukey-style outlier bounds.

    The bounds are defined as:

    .. math:: [Q1 - k \\cdot IQR, Q3 + k \\cdot IQR]

    Parameters
    ----------
    series : pd.Series
        Input data series.

    k : float
        Multiplier applied to the interquartile range.

    Returns
    -------
    OutlierBounds
        Lower and upper outlier boundaries.
    """

    q1 = series.quantile(q=0.25)
    q3 = series.quantile(q=0.75)
    iqr_val = q3 - q1

    lower = q1 - k * iqr_val
    upper = q3 + k * iqr_val

    return OutlierBounds(
        lower=lower,
        upper=upper
    )


def outlier_mask(
    series: pd.Series,
    k: float
) -> pd.Series:
    """
    Identify outliers using Tukey bounds.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    k : float
        Multiplier applied to the interquartile range.

    Returns
    -------
    pd.Series
        Boolean mask where True indicates an outlier.
    """

    bounds = outlier_bounds(series=series, k=k)

    return (series < bounds.lower) | (series > bounds.upper)


def histogram_bins(
    series: pd.Series,
    bins: int
) -> HistogramResult:
    """
    Compute histogram summary statistics.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    bins : int
        Number of histogram bins.

    Returns
    -------
    HistogramResult
        Histogram counts and bin edges.
    """

    clean = series.dropna()

    counts, edges = np.histogram(a=clean, bins=bins)

    return HistogramResult(
        counts=counts,
        bin_edges=edges,
        bins=bins
    )


def empirical_cdf(series: pd.Series) -> EmpiricalCDFResult:
    """
    Compute empirical cumulative distribution function.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    EmpiricalCDFResult
        Sorted values and their empirical cumulative probabilities.
    """

    clean = series.dropna().sort_values()

    cdf = np.arange(1, stop=len(clean) + 1) / len(clean)

    return EmpiricalCDFResult(
        values=clean.to_numpy(dtype=float),
        cdf=cdf
    )
