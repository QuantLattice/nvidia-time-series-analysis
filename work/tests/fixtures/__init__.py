"""Test data fixtures package.

This package contains reusable pandas DataFrame fixtures used for testing
data processing, validation, and normalization pipelines.

Fixtures simulate both clean and dirty datasets to ensure robustness of
data handling logic.
"""


from work.tests.fixtures.dataframes import valid_df, raw_df
from work.tests.fixtures.controller import (
    controller,
    created_quote_ids,
)


__all__ = [
    "valid_df",
    "raw_df",
    "controller",
    "created_quote_ids",
]
