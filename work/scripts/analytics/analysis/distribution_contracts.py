"""
Data contracts for distribution-oriented analysis.

This module defines structured result types returned by the
distribution analysis layer.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
from typing import Mapping

from work.scripts.analytics.statistics import (
    OutlierBounds,
    HistogramResult,
    EmpiricalCDFResult
)


@dataclass(frozen=True)
class DistributionAnalysisReport:
    """
    Distribution summary report for a single Series.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    name : str
        Resolved series name.

    quantiles : Mapping[float, float]
        Mapping between quantile probabilities and corresponding
        estimated values.

    iqr : float
        Interquartile range.

    outlier_bounds : OutlierBounds
        Lower and upper Tukey outlier boundaries.

    outlier_count : int
        Number of detected outliers.

    outlier_ratio : float
        Share of observations classified as outliers.

    histogram : HistogramResult
        Histogram bin counts and edges.

    empirical_cdf : EmpiricalCDFResult
        Empirical cumulative distribution function values.
    """

    name: str

    quantiles: Mapping[float, float]

    iqr: float

    outlier_bounds: OutlierBounds
    outlier_count: int
    outlier_ratio: float

    histogram: HistogramResult

    empirical_cdf: EmpiricalCDFResult
