"""Pandas DataFrame wrapper for StockQuote dataset.

This module provides a typed interface over pandas DataFrame for safer
and more readable access to stock price data columns.
"""


import pandas as pd
from .stock_quote_schema import StockQuoteSchema as S


class StockQuoteFrame:
    """Wrapper around pandas DataFrame for StockQuote data.

    Parameters
    ----------
    df : pd.DataFrame
        Raw stock quote dataset.
    """

    def __init__(self, df: pd.DataFrame):
        """Initialize wrapper with DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset.
        """
        self._df = df

    @property
    def df(self) -> pd.DataFrame:
        """Return underlying DataFrame."""
        return self._df

    @property
    def trade_date(self) -> pd.Series:
        """Trade date column."""
        return self._df[S.TRADE_DATE]

    @property
    def source(self) -> pd.Series:
        """Source column."""
        return self._df[S.SOURCE]

    @property
    def open_price(self) -> pd.Series:
        """Open price column."""
        return self._df[S.OPEN_PRICE]

    @property
    def high_price(self) -> pd.Series:
        """High price column."""
        return self._df[S.HIGH_PRICE]

    @property
    def low_price(self) -> pd.Series:
        """Low price column."""
        return self._df[S.LOW_PRICE]

    @property
    def close_price(self) -> pd.Series:
        """Close price column."""
        return self._df[S.CLOSE_PRICE]

    @property
    def adj_close_price(self) -> pd.Series:
        """Adjusted close price column."""
        return self._df[S.ADJ_CLOSE_PRICE]

    @property
    def volume(self) -> pd.Series:
        """Trading volume column."""
        return self._df[S.VOLUME]
