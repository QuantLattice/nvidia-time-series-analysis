"""
Contracts for descriptive statistics analysis.

This module defines the result dataclass for single-series
descriptive statistical reports.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass


@dataclass(frozen=True)
class SeriesDescriptiveReport:
    """
    Descriptive summary for a single pandas Series.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    name : str
        Resolved series name.

    mean : float
        Arithmetic mean.

    median : float
        Median value.

    variance : float
        Sample variance.

    std : float
        Sample standard deviation.

    data_range : float
        Difference between maximum and minimum values.

    min : float
        Minimum value.

    max : float
        Maximum value.

    skewness : float
        Sample skewness.

    kurtosis : float
        Sample kurtosis.

    missing_count : int
        Number of missing observations.

    missing_ratio : float
        Share of missing observations.

    positive_ratio : float
        Share of values greater than zero.

    negative_ratio : float
        Share of values less than zero.

    zero_ratio : float
        Share of values equal to zero.

    trimmed_mean : float
        Mean after trimming the distribution tails.

    mad : float
        Median absolute deviation.

    coefficient_of_variation : float
        Ratio of standard deviation to mean.
    """

    name: str

    mean: float
    median: float

    variance: float
    std: float

    data_range: float
    min: float
    max: float

    skewness: float
    kurtosis: float

    missing_count: int
    missing_ratio: float

    positive_ratio: float
    negative_ratio: float
    zero_ratio: float

    trimmed_mean: float
    mad: float

    coefficient_of_variation: float
