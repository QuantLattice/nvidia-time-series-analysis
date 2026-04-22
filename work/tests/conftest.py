"""Pytest configuration and shared test fixtures.

This module exposes commonly used fixtures for the entire test suite.
It acts as a central registry for reusable test data to avoid duplication
across test modules.

Fixtures provided here are automatically discovered by pytest.
"""


from work.tests.fixtures import (
    controller,
    created_quote_ids,
    raw_df,
    valid_df,
)


__all__ = [
    "valid_df",
    "raw_df",
    "controller",
    "created_quote_ids",
]
