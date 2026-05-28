"""
Time-series train/test splitting utilities.

This module provides deterministic chronological splitting
for time-series datasets.

Unlike random splits, chronological splitting preserves
temporal ordering, making it suitable for:

- forecasting model validation;
- backtesting strategies;
- leakage-safe dataset construction.
"""


from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class TrainTestSplitResult:
    """
    Result of chronological train/test split.

    Attributes
    ----------
    train : pd.Series
        Training portion of the series (earlier time steps).

    test : pd.Series
        Test portion of the series (later time steps).
    """

    train: pd.Series
    test: pd.Series


def chronological_split(
    series: pd.Series,
    test_ratio: float
) -> TrainTestSplitResult:
    """
    Split a time series into train and test sets preserving order.

    The split is performed chronologically, using the earliest
    portion for training and the latest portion for testing.

    Parameters
    ----------
    series : pd.Series
        Input time series sorted in temporal order.

    test_ratio : float
        Fraction of data to use as test set.
        Must be between 0 and 1 (exclusive).

    Returns
    -------
    TrainTestSplitResult
        Object containing train and test splits.

    Raises
    ------
    ValueError
        If test_ratio is not in (0, 1) or series is too short.

    Notes
    -----
    - No shuffling is performed.
    - Ensures at least one observation in both train and test sets.
    """

    if not 0 < test_ratio < 1:
        raise ValueError(
            "test_ratio must be between 0 and 1."
        )

    n = len(series)

    if n < 2:
        raise ValueError(
            "Series must contain at least 2 elements for train/test split."
        )

    split_index = int(n * (1 - test_ratio))

    if split_index < 1:
        split_index = 1

    if split_index >= n:
        split_index = n - 1

    return TrainTestSplitResult(
        train=series.iloc[:split_index],
        test=series.iloc[split_index:]
    )
