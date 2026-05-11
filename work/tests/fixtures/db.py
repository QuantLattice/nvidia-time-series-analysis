"""MySQL database fixtures for testing.

Connects to the real VPS MySQL database using credentials from .env.
Each test runs inside a transaction that is rolled back on completion,
ensuring full isolation without leaving any data behind.
"""

import os
from pathlib import Path
from typing import Any, Generator

import pytest
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from work.scripts.db import Base


def _mysql_url() -> str:
    project_root = Path(__file__).resolve().parents[3]
    load_dotenv(project_root / ".env")

    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    host = os.getenv("MYSQL_HOST", "localhost")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DB", "nvidia_timeseries")

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"


@pytest.fixture(scope="session")
def engine() -> Generator[Engine, Any, None]:
    """Create a shared MySQL engine for the test session."""

    _engine = create_engine(_mysql_url())

    yield _engine

    _engine.dispose()


@pytest.fixture(scope="session")
def create_schema(engine: Engine) -> Generator[None, Any, None]:
    """Ensure all ORM tables exist before any test runs.

    Notes
    -----
    Uses CREATE TABLE IF NOT EXISTS semantics — safe on a non-empty database.
    Tables are never dropped so real data is never at risk.
    """

    Base.metadata.create_all(bind=engine)

    yield


@pytest.fixture
def db_session(engine: Engine, create_schema: None) -> Generator[Session, None, None]:
    """Provide a per-test transactional session that rolls back on teardown.

    Notes
    -----
    - Each test runs inside a transaction.
    - Changes are rolled back after the test completes.
    - Ensures full test isolation without touching committed data.
    """

    connection = engine.connect()
    transaction = connection.begin()

    session = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
