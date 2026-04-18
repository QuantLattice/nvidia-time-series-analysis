"""Environment loader for application database settings.

This module loads variables from a .env file and builds a typed database
configuration object with sensible default values for local development.
"""

from dataclasses import dataclass
from dotenv import load_dotenv
import os
from pathlib import Path


@dataclass(frozen=True)
class DBConfig:
    """Database connection settings.

    Attributes
    ----------
    user : str
        Database user name.
    password : str
        Database user password.
    host : str
        Database host address.
    port : int
        Database port number.
    database : str
        Database name.
    """

    user: str
    password: str
    host: str
    port: int
    database: str


class EnvLoader:
    """Load environment variables from a .env file.

    Parameters
    ----------
    env_path : str | Path | None
        Path to the .env file. If None, the file is resolved from the
        project root.
    """

    def __init__(self, env_path: str | Path | None) -> None:
        """Initialize the environment loader and load variables.

        Parameters
        ----------
        env_path : str | Path | None
            Path to the .env file. If None, the default file located in the
            project root is used.
        """

        if env_path is None:
            project_root = Path(__file__).resolve().parents[3]
            env_path = project_root / ".env"
        load_dotenv(env_path)

    def get_db_config(self) -> DBConfig:
        """Build database configuration from environment variables.

        Returns
        -------
        DBConfig
            Database configuration populated from environment variables or
            fallback defaults.
        """

        return DBConfig(
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            database=os.getenv("MYSQL_DB", "nvidia_timeseries")
        )
