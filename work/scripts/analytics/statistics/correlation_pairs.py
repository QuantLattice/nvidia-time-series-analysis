"""
Correlation matrix construction and pair extraction utilities.

This module provides helpers for building a correlation matrix,
extracting pairwise records from it, filtering by strength, and
ranking top positive and negative correlations.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

import pandas as pd
from typing import List, Literal

from work.scripts.analytics.statistics.correlation_analysis import (
    CorrelationMatrixResult,
    CorrelationPair,
)


def correlation_matrix(
    df: pd.DataFrame,
    method: Literal['pearson', 'kendall', 'spearman']
) -> CorrelationMatrixResult:
    """Build a correlation matrix for numeric columns.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """
    numeric_df = df.select_dtypes(include="number")
    matrix = numeric_df.corr(method=method)
    return CorrelationMatrixResult(method=method, matrix=matrix)


def correlation_pairs(
    matrix: pd.DataFrame
) -> List[CorrelationPair]:
    """Convert a correlation matrix into unique pairwise records.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """
    from typing import cast
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


def strong_correlation(
    pairs: List[CorrelationPair],
    threshold: float
) -> List[CorrelationPair]:
    """Filter pairs by absolute correlation strength.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """
    return [
        pair
        for pair in pairs
        if abs(pair.correlation) >= threshold
    ]


def top_positive_correlations(
    pairs: List[CorrelationPair],
    n: int
) -> List[CorrelationPair]:
    """Return the n strongest positive correlations.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """
    positive = [p for p in pairs if p.correlation > 0]
    return sorted(
        positive,
        key=lambda p: p.correlation,
        reverse=True
    )[:n]


def top_negative_correlations(
    pairs: List[CorrelationPair],
    n: int
) -> List[CorrelationPair]:
    """Return the n strongest negative correlations.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """
    negative = [p for p in pairs if p.correlation < 0]
    return sorted(
        negative,
        key=lambda p: p.correlation
    )[:n]


__all__ = [
    "correlation_matrix",
    "correlation_pairs",
    "strong_correlation",
    "top_positive_correlations",
    "top_negative_correlations",
]
