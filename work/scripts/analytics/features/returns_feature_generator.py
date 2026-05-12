"""
Feature generator for return-based analytics.

This module provides a reusable generator that enriches a price-based
DataFrame with daily, log, cumulative, and rolling return features.
"""


import pandas as pd
from typing import Optional, List

from work.scripts.analytics.constants import ROLLING_WINDOWS
from work.scripts.contracts import AnalyticsFeatureNames as FN
from work.scripts.analytics.indicators import (
    daily_return,
    log_return,
    cumulative_return,
    rolling_return
)


class ReturnsFeatureGenerator:
    """
    Generate return-based analytical features.

    Parameters
    ----------
    windows : Sequence[int] | None, optional
        Rolling windows used for rolling return generation.
        If omitted, default analytics windows are used.
    """

    def __init__(
        self,
        windows: Optional[List[int]] = None
    ) -> None:
        """
        Initialize the feature generator.

        Parameters
        ----------
        windows : Sequence[int] | None, optional
            Rolling windows used for rolling return generation.
        """

        self.windows = windows or ROLLING_WINDOWS

    def apply(
        self,
        df: pd.DataFrame,
        price_column: str
    ) -> pd.DataFrame:
        """
        Add return-based features to a DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Source DataFrame containing price data.

        price_column : str
            Name of the column with price values.

        Returns
        -------
        pd.DataFrame
            Copy of the input DataFrame enriched with return features.
        """

        result = df.copy()

        price_series = result[price_column]

        result[FN.DAILY_RETURN] = daily_return(series=price_series)

        result[FN.LOG_RETURN] = log_return(series=price_series)

        result[FN.CUMULATIVE_RETURN] = cumulative_return(series=price_series)

        for window in self.windows:
            column_name = FN.rolling_return(window=window)

            result[column_name] = rolling_return(
                series=price_series,
                window=window
            )

        return result
