"""DataFrame factory for StockQuote test datasets.

This module provides reusable pandas DataFrame generators for testing
normalization, validation, and repository-related data flows.

The factory includes both clean and intentionally malformed datasets in
order to cover positive and negative test scenarios.
"""


import pandas as pd

from work.scripts.contracts.schemas import StockQuoteSchema as S


class DataFrameFactory:
    """Factory for generating StockQuote DataFrames used in tests."""

    @staticmethod
    def valid(rows: int = 1) -> pd.DataFrame:
        """Create a clean, schema-compliant DataFrame.

        Parameters
        ----------
        rows : int, default=1
            Number of rows to generate.

        Returns
        -------
        pd.DataFrame
            Valid dataset with correct column names, types, and values.
        """

        return pd.DataFrame(
            {
                S.TRADE_DATE: pd.date_range("2024-01-01", periods=rows),
                S.SOURCE: ["example.com"] * rows,
                S.OPEN_PRICE: [100.0] * rows,
                S.HIGH_PRICE: [110.0] * rows,
                S.LOW_PRICE: [90.0] * rows,
                S.CLOSE_PRICE: [105.0] * rows,
                S.ADJ_CLOSE_PRICE: [105.0] * rows,
                S.VOLUME: [1000] * rows,
            }
        )

    @staticmethod
    def raw_unsorted() -> pd.DataFrame:
        """Create a dirty CSV-like DataFrame.

        Returns
        -------
        pd.DataFrame
            Dataset containing whitespace in headers, unsorted dates, string
            values, and a missing date value.
        """

        return pd.DataFrame(
            {
                " trade_date ": [
                    "2024-01-02",
                    "2024-01-01",
                    None,
                    "2024-02-02",
                ],
                " source ": ["example.com", "manually", "", "s1"],
                "open_price": ["100", "101", "77", "50"],
                "high_price": ["110", "111", "79", "55"],
                "low_price": ["90", "91", "75", "33"],
                "close_price": ["105", "106", "76", "52"],
                "adj_close_price": ["105", "106", None, None],
                "volume": ["1000", "2000", "112", "123"],
            }
        )

    @staticmethod
    def with_invalid_datetime() -> pd.DataFrame:
        """Create a dataset with an invalid date string.

        Returns
        -------
        pd.DataFrame
            Dataset where at least one value in trade date column cannot be
            converted to datetime.
        """

        return pd.DataFrame(
            {
                S.TRADE_DATE: ["2024-25-2044", "2024-01-02", "2024-01-03"],
                S.SOURCE: ["example.com", "manually", "s1"],
                S.OPEN_PRICE: ["80", "50", "120"],
                S.HIGH_PRICE: ["110", "70", "100"],
                S.LOW_PRICE: ["90", "60", "90"],
                S.CLOSE_PRICE: ["105", "65", "95"],
                S.ADJ_CLOSE_PRICE: ["105", None, "96"],
                S.VOLUME: ["1000", "100", "2000"],
            }
        )

    @staticmethod
    def with_invalid_string() -> pd.DataFrame:
        """Create a dataset with a non-string value in the source column.

        Returns
        -------
        pd.DataFrame
            Dataset where the source column contains a non-text value.
        """

        return pd.DataFrame(
            {
                S.TRADE_DATE: ["2024-01-01", "2024-01-02", "2024-01-03"],
                S.SOURCE: ["example.com", "manually", {"key": "value"}],
                S.OPEN_PRICE: ["80", "50", "120"],
                S.HIGH_PRICE: ["110", "70", "100"],
                S.LOW_PRICE: ["90", "60", "90"],
                S.CLOSE_PRICE: ["105", "65", "95"],
                S.ADJ_CLOSE_PRICE: ["105", None, "96"],
                S.VOLUME: ["1000", "100", "2000"],
            }
        )

    @staticmethod
    def with_invalid_numeric() -> pd.DataFrame:
        """Create a dataset with an invalid numeric value.

        Returns
        -------
        pd.DataFrame
            Dataset where a price column contains a non-numeric string.
        """

        return pd.DataFrame(
            {
                S.TRADE_DATE: ["2024-01-01", "2024-01-02", "2024-01-03"],
                S.SOURCE: ["example.com", "manually", "s1"],
                S.OPEN_PRICE: ["bad", "50", "120"],
                S.HIGH_PRICE: ["110", "70", "100"],
                S.LOW_PRICE: ["90", "60", "90"],
                S.CLOSE_PRICE: ["105", "65", "95"],
                S.ADJ_CLOSE_PRICE: ["105", None, "96"],
                S.VOLUME: ["1000", "100", "2000"],
            }
        )

    @staticmethod
    def with_invalid_integer() -> pd.DataFrame:
        """Create a dataset with an invalid integer value.

        Returns
        -------
        pd.DataFrame
            Dataset where the volume column contains a non-integer string.
        """

        return pd.DataFrame(
            {
                S.TRADE_DATE: ["2024-01-01", "2024-01-02", "2024-01-03"],
                S.SOURCE: ["example.com", "manually", "s1"],
                S.OPEN_PRICE: ["60", "50", "120"],
                S.HIGH_PRICE: ["110", "70", "100"],
                S.LOW_PRICE: ["90", "60", "90"],
                S.CLOSE_PRICE: ["105", "65", "95"],
                S.ADJ_CLOSE_PRICE: ["105", None, "96"],
                S.VOLUME: ["1000", "100", "bad"],
            }
        )

    @staticmethod
    def missing_values() -> pd.DataFrame:
        """Create a dataset with missing values in required fields.

        Returns
        -------
        pd.DataFrame
            Dataset containing null-like and empty values in key columns.
        """

        return pd.DataFrame(
            {
                S.TRADE_DATE: ["2024-01-01", None],
                S.SOURCE: ["example.com", ""],
                S.OPEN_PRICE: ["100", "101"],
                S.HIGH_PRICE: ["110", "111"],
                S.LOW_PRICE: ["90", "91"],
                S.CLOSE_PRICE: ["105", "106"],
                S.ADJ_CLOSE_PRICE: ["105", "106"],
                S.VOLUME: ["1000", "2000"],
            }
        )
