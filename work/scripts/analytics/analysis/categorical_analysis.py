"""
Categorical feature analysis utilities for exploratory data analysis.

This module provides high-level analytical abstractions for categorical
data inspection based on reusable statistical primitives from
``work.scripts.analytics.statistics``.

The analysis layer combines:
- category distribution analysis;
- dominant category detection;
- entropy estimation;
- class imbalance evaluation;
- missing value analysis.
"""


from dataclasses import dataclass
import pandas as pd
from typing import Mapping, Union, overload

from work.scripts.analytics.statistics import (
    CategoryDistribution,
    category_distribution,
    dominant_category,
    category_entropy,
    imbalance_ratio
)
from work.scripts.analytics.utils import resolve_series_name


@dataclass(frozen=True)
class CategoricalAnalysisReport:
    """
    Container with categorical analysis results for a single series.

    Attributes
    ----------
    name : str
        Name of the analyzed series.

    distribution : CategoryDistribution
        Category frequency counts and normalized ratios.

    dominant_category : str
        Most frequently occurring category.

    entropy : float
        Shannon entropy of the categorical distribution.

    imbalance_ratio : float
        Ratio between the largest and smallest category frequencies.

    unique_categories : int
        Number of unique non-missing categories.

    missing_count : int
        Number of missing values.

    missing_ratio : float
        Fraction of missing observations.
    """

    name: str

    distribution: CategoryDistribution

    dominant_category: str

    entropy: float

    imbalance_ratio: float

    unique_categories: int

    missing_count: int

    missing_ratio: float


class CategoricalAnalysis:
    """
    High-level categorical data analysis interface.

    This class combines multiple categorical statistics into a single
    analytical workflow suitable for exploratory data analysis (EDA)
    and dataset diagnostics.
    """

    @overload
    def analyze(
        self,
        data: pd.Series
    ) -> CategoricalAnalysisReport:
        """
        Analyze a single categorical series.

        Parameters
        ----------
        data : pd.Series
            Input categorical series.

        Returns
        -------
        CategoricalAnalysisReport
            Analysis report for the provided series.
        """
        ...

    @overload
    def analyze(
        self,
        data: pd.DataFrame
    ) -> Mapping[str, CategoricalAnalysisReport]:
        """
        Analyze all categorical columns in a DataFrame.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame containing categorical features.

        Returns
        -------
        Mapping[str, CategoricalAnalysisReport]
            Mapping between column names and their corresponding
            categorical analysis reports.
        """
        ...

    def analyze(
        self,
        data: Union[pd.Series, pd.DataFrame]
    ) -> Union[
        CategoricalAnalysisReport,
        Mapping[str, CategoricalAnalysisReport]
    ]:
        """
        Analyze categorical data.

        Parameters
        ----------
        data : Union[pd.Series, pd.DataFrame]
            Input categorical data structure.

        Returns
        -------
        Union[
            CategoricalAnalysisReport,
            Mapping[str, CategoricalAnalysisReport]
        ]
            Analysis report for a single series or mapping of reports
            for DataFrame columns.
        """

        if isinstance(data, pd.DataFrame):
            return self._analyze_dataframe(df=data)

        return self._analyze_series(series=data)

    def _analyze_series(
        self,
        series: pd.Series
    ) -> CategoricalAnalysisReport:
        """
        Analyze a single categorical series.

        Parameters
        ----------
        series : pd.Series
            Input categorical series.

        Returns
        -------
        CategoricalAnalysisReport
            Structured categorical analysis report.
        """

        distribution = category_distribution(series=series)

        return CategoricalAnalysisReport(
            name=resolve_series_name(series=series),

            distribution=distribution,

            dominant_category=dominant_category(
                series=series
            ),

            entropy=category_entropy(
                series=series
            ),

            imbalance_ratio=imbalance_ratio(
                series=series
            ),

            unique_categories=int(
                series.dropna().nunique()
            ),

            missing_count=int(
                series.isna().sum()
            ),

            missing_ratio=float(
                series.isna().mean()
            )
        )

    def _analyze_dataframe(
        self,
        df: pd.DataFrame
    ) -> Mapping[str, CategoricalAnalysisReport]:
        """
        Analyze all categorical columns in a DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame containing categorical features.

        Returns
        -------
        Mapping[str, CategoricalAnalysisReport]
            Mapping between column names and their corresponding
            categorical analysis reports.
        """

        return {
            column: self._analyze_series(
                series=df[column]
            )
            for column in df.columns
        }
