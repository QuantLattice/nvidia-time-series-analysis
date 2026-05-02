"""In-memory database fixtures for unit testing.

This module configures a temporary SQLite database used exclusively
for automated tests.

It provides:
- SQLAlchemy engine (in-memory)
- schema initialization and teardown
- transactional session isolation per test

Each test runs inside a rollback-safe transaction ensuring full isolation.
"""


import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, Session

from work.scripts.db import Base

from sqlalchemy import Engine
from typing import Generator, Any


@pytest.fixture(scope="session")
def engine() -> Generator[Engine, Any, None]:
    """Create a shared in-memory SQLite engine for test session."""

    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    yield engine

    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def create_schema(
    engine: Engine
) -> Generator[None, Any, None]:
    """Create and destroy database schema for test session lifetime."""

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(
    engine: Engine
) -> Generator[Session, None, None]:
    """Provide transactional database session for each test.

    Notes
    -----
    - Each test runs inside a transaction
    - Changes are rolled back after test completion
    - Ensures full test isolation
    """

    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
