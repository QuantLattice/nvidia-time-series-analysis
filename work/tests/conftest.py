"""Pytest global configuration module.

This module exposes shared test fixtures that are available across the
entire test suite.

It serves as a central entry point for database-related fixtures such as:
- in-memory SQLAlchemy engine
- schema creation and teardown hooks
- transactional test sessions

Pytest discovers this module automatically without explicit imports.
"""


from work.tests.fixtures import (
    engine,
    create_schema,
    db_session
)


__all__ = [
    "engine",
    "create_schema",
    "db_session",
]
