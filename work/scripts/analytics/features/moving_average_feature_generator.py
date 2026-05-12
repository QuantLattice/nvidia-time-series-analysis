"""
Feature generator for moving average indicators.

This module provides a reusable generator that enriches a price-based
DataFrame with simple, exponential, and volume-weighted moving
average features.
"""


import pandas as pd
from typing import Optional, List

from work.scripts.analytics.constants import (
    EMA_WINDOWS,
    SMA_WINDOWS,
    VWMA_WINDOWS
)
from work.scripts.analytics.indicators import (
    sma,
    ema,
    vwma
)
from work.scripts.contracts import AnalyticsFeatureNames as FN


class MovingAverageFeatureGenerator:
    """
    Generate moving average analytical features.

    Parameters
    ----------
    sma_windows : Optional[List[int]], optional
        Window sizes used for simple moving average generation.

    ema_windows : Optional[List[int]], optional
        Window sizes used for exponential moving average generation.

    vwma_windows : Optional[List[int]], optional
        Window sizes used for volume-weighted moving average generation.
    """

    def __init__(
        self,
        sma_windows: Optional[List[int]] = None,
        ema_windows: Optional[List[int]] = None,
        vwma_windows: Optional[List[int]] = None
    ) -> None:
        """
        Initialize moving average feature generator.

        Parameters
        ----------
        sma_windows : Optional[List[int]], optional
            Window sizes used for SMA feature generation.

        ema_windows : Optional[List[int]], optional
            Window sizes used for EMA feature generation.

        vwma_windows : Optional[List[int]], optional
            Window sizes used for VWMA feature generation.
        """

        self.sma_windows = sma_windows or SMA_WINDOWS
        self.ema_windows = ema_windows or EMA_WINDOWS
        self.vwma_windows = vwma_windows or VWMA_WINDOWS

    def apply(
        self,
        df: pd.DataFrame,
        price_column: str,
        volume_column: str
    ) -> pd.DataFrame:
        """
        Add moving average features to a DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Source DataFrame containing market data.

        price_column : str
            Name of the column containing price values.

        volume_column : str
            Name of the column containing trading volume values.

        Returns
        -------
        pd.DataFrame
            Copy of the input DataFrame enriched with moving
            average features.
        """

        result = df.copy()
        price_series = result[price_column]
        volume_series = result[volume_column]

        for window in self.sma_windows:
            column_name = FN.sma(window=window)
            result[column_name] = sma(
                series=price_series,
                window=window
            )

        for window in self.ema_windows:
            column_name = FN.ema(window=window)
            result[column_name] = ema(
                series=price_series,
                window=window
            )

        for window in self.vwma_windows:
            column_name = FN.vwma(window=window)

            result[column_name] = vwma(
                price_series=price_series,
                volume_series=volume_series,
                window=window
            )

        return result
