"""Standardized schema definition for StockQuote dataset.

This module defines a unified set of column name constants used across
the entire application, including:

- Database ORM mapping
- pandas DataFrame transformations
- Analytics and reporting layer
- Data validation routines

The schema also includes metadata fields (e.g., data source) that allow
tracking provenance of imported records.
"""


class StockQuoteSchema:
    """Column schema for stock price time series dataset.

    This class defines standardized column names and grouped subsets of
    columns used for analytical processing, validation, and data lineage.

    Notes
    -----
    - All attributes are immutable constants.
    - Serves as a single source of truth for dataset structure.
    - Includes both numerical market data and metadata fields.
    """

    # ---------------------------
    # CORE COLUMN NAMES
    # ---------------------------

    """Trading date of the stock record."""
    TRADE_DATE = "trade_date"

    """Data source identifier (e.g., CSV filename, provider name, or URL)."""
    SOURCE = "source"

    """Opening price of the stock for the trading day."""
    OPEN_PRICE = "open_price"

    """Highest price during the trading day."""
    HIGH_PRICE = "high_price"

    """Lowest price during the trading day."""
    LOW_PRICE = "low_price"

    """Closing price of the stock for the trading day."""
    CLOSE_PRICE = "close_price"

    """Adjusted closing price accounting for corporate actions."""
    ADJ_CLOSE_PRICE = "adj_close_price"

    """Number of shares traded during the trading day."""
    VOLUME = "volume"

    # ---------------------------
    # COLUMN GROUPS
    # ---------------------------

    """Complete ordered list of all dataset columns."""
    ALL_COLUMNS = [
        TRADE_DATE,
        SOURCE,
        OPEN_PRICE,
        HIGH_PRICE,
        LOW_PRICE,
        CLOSE_PRICE,
        ADJ_CLOSE_PRICE,
        VOLUME,
    ]

    """Columns representing continuous numeric price values."""
    NUMERIC_COLUMNS = [
        OPEN_PRICE,
        HIGH_PRICE,
        LOW_PRICE,
        CLOSE_PRICE,
        ADJ_CLOSE_PRICE,
    ]

    """Columns representing integer-based values (e.g., trading volume)."""
    INTEGER_COLUMNS = [
        VOLUME,
    ]

    """Columns representing textual data (e.g., data source identifiers)."""
    STRING_COLUMNS = [
        SOURCE,
    ]

    """Minimum required columns for a valid stock dataset.

    Notes
    -----
    Adjusted close price is optional and may be missing in raw datasets.
    """
    REQUIRED_COLUMNS = [
        TRADE_DATE,
        SOURCE,
        OPEN_PRICE,
        HIGH_PRICE,
        LOW_PRICE,
        CLOSE_PRICE,
        VOLUME,
    ]
