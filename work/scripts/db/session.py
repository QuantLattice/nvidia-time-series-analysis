"""Database engine and session management utilities.

This module provides functionality for building a database connection URL,
initializing the SQLAlchemy engine, and managing database sessions using
a context manager.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from work.library.config.config_manager import ConfigManager
from work.library.config.env_loader import DBConfig

from pathlib import Path
from urllib.parse import quote_plus


def build_db_url(db_config: DBConfig) -> str:
    """Build a SQLAlchemy database connection URL.

    Parameters
    ----------
    db_config : DBConfig
        Database configuration object containing connection parameters.

    Returns
    -------
    str
        SQLAlchemy-compatible database connection string.

    Notes
    -----
    The password is URL-encoded to ensure safe usage in the connection string.
    """

    password = quote_plus(db_config.password)

    return (
        f"mysql+pymysql://{db_config.user}:{password}"
        f"@{db_config.host}:{db_config.port}/{db_config.database}"
    )


class Database:
    """Database connection and session factory.

    This class initializes the SQLAlchemy engine and provides a session
    factory for interacting with the database.

    Parameters
    ----------
    env_path : str | None, optional
        Path to the .env file with database credentials.
    app_config_path : str | Path | None, optional
        Path to the application configuration file.

    Attributes
    ----------
    db_url : str
        Database connection URL.
    engine : sqlalchemy.Engine
        SQLAlchemy engine instance.
    SessionLocal : sessionmaker
        Factory for creating database sessions.
    """

    def __init__(
        self,
        env_path: str | None = None,
        app_config_path: str | Path | None = None
    ) -> None:
        """Initialize the database connection.

        Parameters
        ----------
        env_path : str | None, optional
            Path to the .env file.
        app_config_path : str | Path | None, optional
            Path to the application configuration file.
        """

        config = ConfigManager(
            env_path=env_path,
            app_config_path=app_config_path
        ).load()

        self.db_url = build_db_url(config.db)

        self.engine = create_engine(
            url=self.db_url,
            echo=False,
            pool_pre_ping=True
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False
        )

    @contextmanager
    def session(self):
        """Provide a transactional database session.

        Yields
        ------
        sqlalchemy.orm.Session
            Active database session.

        Notes
        -----
        - Commits transaction if no exceptions occur.
        - Rolls back transaction on error.
        - Always closes the session after use.

        Examples
        --------
        >>> db = Database()
        >>> with db.session() as session:
        ...     session.execute("SELECT 1")
        """

        db = self.SessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
