"""
Central tendency statistics for exploratory data analysis.

This module provides mean and median estimators for pandas Series.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


import pandas as pd


def mean(series: pd.Series) -> float:
    """
    Calculate the arithmetic mean.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Arithmetic mean of the series.
    """

    return series.mean()


def median(series: pd.Series) -> float:
    """
    Calculate the median value.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    Returns
    -------
    float
        Median of the series.
    """

    return series.median()
