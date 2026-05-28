"""
Alternative CSV column names for stock quote datasets.

This module defines known aliases for external input files.
The mapper uses these aliases to resolve user-provided CSV headers
to the internal schema expected by the application pipeline.
"""


class StockQuoteColumnAliases:
    """
    Known aliases for stock quote CSV columns.

    These aliases are used by the mapping stage to resolve incoming
    CSV column names to the internal schema names.

    Attributes
    ----------
    TRADE_DATE : list[str]
        Alternative names for the trade date column.

    OPEN_PRICE : list[str]
        Alternative names for the open price column.

    HIGH_PRICE : list[str]
        Alternative names for the high price column.

    LOW_PRICE : list[str]
        Alternative names for the low price column.

    CLOSE_PRICE : list[str]
        Alternative names for the close price column.

    VOLUME : list[str]
        Alternative names for the trading volume column.
    """

    TRADE_DATE = ["date", "datetime", "timestamp"]
    OPEN_PRICE = ["open", "o"]
    HIGH_PRICE = ["high", "h"]
    LOW_PRICE = ["low", "l"]
    CLOSE_PRICE = ["close", "c"]
    VOLUME = ["volume", "vol"]
