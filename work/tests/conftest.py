"""Pytest global configuration module.

This module registers shared fixtures across the entire test suite.

It serves as a central entry point for:
- Data fixtures (pandas datasets)
- Database fixtures (engine, sessions)
- Schema initialization hooks

Pytest automatically discovers this module without explicit imports.
"""


from work.tests.fixtures import (
    valid_df,
    raw_df,
    engine,
    create_schema,
    db_session
)


__all__ = [
    "valid_df",
    "raw_df",
    "engine",
    "create_schema",
    "db_session"
]
