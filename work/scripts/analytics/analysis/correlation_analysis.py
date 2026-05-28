"""
Correlation analysis abstractions for exploratory data analysis.

This module provides high-level correlation analysis utilities built
on top of the low-level statistical helpers from
``work.scripts.analytics.statistics``.

The analysis layer combines:
- correlation matrix computation;
- pairwise correlation extraction;
- strong correlation filtering;
- ranking of strongest positive and negative relationships.
"""


from dataclasses import dataclass
from typing import List, Literal
import pandas as pd

from work.scripts.analytics.statistics import (
    CorrelationMatrixResult,
    correlation_matrix,
    CorrelationPair,
    correlation_pairs,
    strong_correlation,
    top_positive_correlations,
    top_negative_correlations
)
from work.scripts.analytics.constants import (
    DEFAULT_CORRELATION_METHOD,
    RETURN_STRONG_THRESHOLD,
    DEFAULT_TOP_CORRELATIONS_COUNT
)


@dataclass(frozen=True)
class CorrelationAnalysisReport:
    """
    Container with complete correlation analysis results.

    Attributes
    ----------
    matrix : CorrelationMatrixResult
        Correlation matrix together with the correlation method used.

    pairs : List[CorrelationPair]
        Flattened list of unique pairwise feature correlations.

    strong_pairs : List[CorrelationPair]
        Correlation pairs whose absolute correlation exceeds
        the configured threshold.

    top_positive : List[CorrelationPair]
        Top strongest positive correlation pairs.

    top_negative : List[CorrelationPair]
        Top strongest negative correlation pairs.
    """

    matrix: CorrelationMatrixResult

    pairs: List[CorrelationPair]

    strong_pairs: List[CorrelationPair]

    top_positive: List[CorrelationPair]

    top_negative: List[CorrelationPair]


class CorrelationAnalysis:
    """
    High-level correlation analysis interface.

    This class aggregates multiple correlation-related statistical
    operations into a single analytical workflow.

    The analysis includes:
    - correlation matrix generation;
    - pairwise correlation extraction;
    - strong correlation filtering;
    - ranking of strongest positive and negative correlations.
    """

    def analyze(
        self,
        df: pd.DataFrame,
        method: Literal[
            "pearson",
            "spearman",
            "kendall"
        ] = DEFAULT_CORRELATION_METHOD,
        strong_threshold: float = RETURN_STRONG_THRESHOLD,
        top_n: int = DEFAULT_TOP_CORRELATIONS_COUNT
    ) -> CorrelationAnalysisReport:
        """
        Perform correlation analysis for a DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing numerical features.

        method : {'pearson', 'spearman', 'kendall'}, optional
            Correlation method used for matrix computation.

            Supported methods:
            - ``pearson`` for linear correlation;
            - ``spearman`` for rank correlation;
            - ``kendall`` for ordinal association.

            Default is ``DEFAULT_CORRELATION_METHOD``.

        strong_threshold : float, optional
            Minimum absolute correlation value required for a pair
            to be classified as strongly correlated.

            Default is ``RETURN_STRONG_THRESHOLD``.

        top_n : int, optional
            Number of strongest positive and negative correlations
            to include in the report.

            Default is ``DEFAULT_TOP_CORRELATIONS_COUNT``.

        Returns
        -------
        CorrelationAnalysisReport
            Structured correlation analysis report containing:
            - correlation matrix;
            - pairwise correlations;
            - strong correlations;
            - top positive correlations;
            - top negative correlations.
        """

        matrix_result = correlation_matrix(
            df=df,
            method=method
        )

        pairs = correlation_pairs(
            matrix=matrix_result.matrix
        )

        strong_pairs = strong_correlation(
            pairs=pairs,
            threshold=strong_threshold
        )

        top_positive = top_positive_correlations(
            pairs=pairs,
            n=top_n
        )

        top_negative = top_negative_correlations(
            pairs=pairs,
            n=top_n
        )

        return CorrelationAnalysisReport(
            matrix=matrix_result,

            pairs=pairs,

            strong_pairs=strong_pairs,

            top_positive=top_positive,

            top_negative=top_negative
        )
