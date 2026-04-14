"""Column schema definition for StockQuote data.

This module defines standardized column names used across database
access, pandas transformations, and analytics layers.
"""


class StockQuoteSchema:
    """Column name constants for stock quote dataset."""

    TRADE_DATE = "trade_date"
    OPEN_PRICE = "open_price"
    HIGH_PRICE = "high_price"
    LOW_PRICE = "low_price"
    CLOSE_PRICE = "close_price"
    ADJ_CLOSE_PRICE = "adj_close_price"
    VOLUME = "volume"

    ALL_COLUMNS = [
        TRADE_DATE,
        OPEN_PRICE,
        HIGH_PRICE,
        LOW_PRICE,
        CLOSE_PRICE,
        ADJ_CLOSE_PRICE,
        VOLUME,
    ]
