"""CSV data loading utilities.

This module provides a lightweight abstraction over pandas CSV reading
functionality. It is used as the entry point for importing external
tabular datasets into the application.

The loader is intentionally minimal and does not perform any validation
or transformation. All preprocessing is delegated to higher-level layers
(e.g., contracts/validation).
"""


import pandas as pd


class CSVLoader:
    """Utility class for loading CSV files into pandas DataFrames.

    This class serves as a thin wrapper over `pandas.read_csv`, providing
    a unified entry point for file ingestion across the application.
    """

    @staticmethod
    def load(path: str) -> pd.DataFrame:
        """Load CSV file into a pandas DataFrame.

        Parameters
        ----------
        path : str
            Path to the CSV file.

        Returns
        -------
        pd.DataFrame
            Raw DataFrame containing unprocessed CSV data.

        Notes
        -----
        This function performs no validation, type conversion, or cleaning.
        All transformations are handled in higher layers (normalization and
        validation modules).
        """
        return pd.read_csv(path)
