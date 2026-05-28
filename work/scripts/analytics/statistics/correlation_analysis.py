"""
Correlation analysis utilities for exploratory data analysis.

This module provides pairwise correlation functions, correlation
matrix construction, and helper utilities for extracting and ranking
correlation pairs from a matrix representation.

The functions are intended for use in statistical reporting,
feature screening, and exploratory time-series analysis.
"""


from dataclasses import dataclass
import pandas as pd
import numpy as np
from typing import List, Literal, cast


@dataclass(frozen=True)
class CorrelationMatrixResult:
    """
    Result container for a correlation matrix computation.

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
    """
    Pairwise correlation record.

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
# PAIRWISE CORRELATIONS
# =========================================================

def pearson_correlation(
    series_x: pd.Series,
    series_y: pd.Series
) -> float:
    """
    Calculate Pearson correlation coefficient.

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
    """

    aligned = _aligned_pair(
        series_x=series_x,
        series_y=series_y
    )

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
    """
    Calculate Spearman rank correlation coefficient.

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
    """

    aligned = _aligned_pair(
        series_x=series_x,
        series_y=series_y
    )

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
    """
    Calculate Kendall tau correlation coefficient.

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
    """

    aligned = _aligned_pair(
        series_x=series_x,
        series_y=series_y
    )

    if aligned.empty:
        return np.nan

    return aligned.iloc[:, 0].corr(
        other=aligned.iloc[:, 1],
        method="kendall"
    )


# =========================================================
# CORRELATION MATRIX
# =========================================================

def correlation_matrix(
    df: pd.DataFrame,
    method: Literal['pearson', 'kendall', 'spearman']
) -> CorrelationMatrixResult:
    """
    Calculate a correlation matrix for numeric columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.

    method : {"pearson", "kendall", "spearman"}
        Correlation method used by pandas.

    Returns
    -------
    CorrelationMatrixResult
        Container with the selected method and correlation matrix.
    """

    numeric_df = df.select_dtypes(include="number")

    matrix = numeric_df.corr(method=method)

    return CorrelationMatrixResult(
        method=method,
        matrix=matrix
    )


# =========================================================
# MATRIX EXTRACTION
# =========================================================

def correlation_pairs(
    matrix: pd.DataFrame
) -> List[CorrelationPair]:
    """
    Convert a correlation matrix into pairwise records.

    Parameters
    ----------
    matrix : pd.DataFrame
        Symmetric correlation matrix.

    Returns
    -------
    List[CorrelationPair]
        List of unique feature pairs with correlation values.
    """

    pairs: List[CorrelationPair] = []

    columns = matrix.columns

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            feature_x = columns[i]
            feature_y = columns[j]

            corr = cast(float, matrix.iloc[i, j])

            pairs.append(
                CorrelationPair(
                    feature_x=feature_x,
                    feature_y=feature_y,
                    correlation=corr
                )
            )

    return pairs


# =========================================================
# FILTERING
# =========================================================

def strong_correlation(
    pairs: List[CorrelationPair],
    threshold: float
) -> List[CorrelationPair]:
    """
    Filter correlations by absolute strength.

    Parameters
    ----------
    pairs : List[CorrelationPair]
        Input pairwise correlations.

    threshold : float
        Minimum absolute correlation required to keep a pair.

    Returns
    -------
    List[CorrelationPair]
        Correlation pairs with absolute value greater than or
        equal to the threshold.
    """

    return [
        pair
        for pair in pairs
        if abs(pair.correlation) >= threshold
    ]


# =========================================================
# RANKING
# =========================================================

def top_positive_correlations(
    pairs: List[CorrelationPair],
    n: int
) -> List[CorrelationPair]:
    """
    Return the strongest positive correlations.

    Parameters
    ----------
    pairs : List[CorrelationPair]
        Input pairwise correlations.

    n : int
        Number of top results to return.

    Returns
    -------
    List[CorrelationPair]
        Strongest positive correlations sorted in descending order.
    """

    positive = [
        pair
        for pair in pairs
        if pair.correlation > 0
    ]

    return sorted(
        positive,
        key=lambda pair: pair.correlation,
        reverse=True
    )[:n]


def top_negative_correlations(
    pairs: List[CorrelationPair],
    n: int
) -> List[CorrelationPair]:
    """
    Return the strongest negative correlations.

    Parameters
    ----------
    pairs : List[CorrelationPair]
        Input pairwise correlations.

    n : int
        Number of top results to return.

    Returns
    -------
    List[CorrelationPair]
        Strongest negative correlations sorted from most negative
        to least negative.
    """

    negative = [
        pair
        for pair in pairs
        if pair.correlation < 0
    ]

    return sorted(
        negative,
        key=lambda pair: pair.correlation
    )[:n]


# ==========================================
# INTERNAL HELPERS
# ==========================================

def _aligned_pair(
    series_x: pd.Series,
    series_y: pd.Series,
) -> pd.DataFrame:
    """
    Align two series and drop missing values.

    Parameters
    ----------
    series_x : pd.Series
        First input series.

    series_y : pd.Series
        Second input series.

    Returns
    -------
    pd.DataFrame
        Two-column DataFrame with aligned non-missing values.
    """

    return pd.concat(
        objs=[series_x, series_y],
        axis=1,
    ).dropna()
