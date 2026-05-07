"""
Environment variable manager for database configuration.

This module provides tools for:
- loading environment variables from a .env file;
- building typed database configuration objects;
- resolving default project environment paths;
- providing fallback values for local development.

The environment configuration is primarily used by the
database and infrastructure layers of the application.
"""


from dataclasses import dataclass
from dotenv import load_dotenv
import os
from pathlib import Path
from typing import (
    Optional,
    Union
)


@dataclass(slots=True)
class DBConfig:
    """
    Database connection settings.

    Attributes
    ----------
    user : str
        Database user name.

    password : str
        Database user password.

    host : str
        Database host address.

    port : int
        Database server port number.

    database : str
        Database name.
    """

    user: str
    password: str
    host: str
    port: int
    database: str


class EnvManager:
    """
    Load environment variables from a .env file.

    The loader initializes application environment variables
    and provides typed access to database configuration values.

    Parameters
    ----------
    env_path : Optional[Union[str, Path]], optional
        Path to the .env file. If omitted, the file is resolved
        automatically from the project root directory.
    """

    def __init__(self, env_path: Optional[Union[str, Path]]) -> None:
        """
        Initialize the environment loader.

        Parameters
        ----------
        env_path : Optional[Union[str, Path]], optional
            Path to the .env file. If omitted, the default
            project-level .env file is used.
        """

        if env_path is None:
            project_root = Path(__file__).resolve().parents[3]
            env_path = project_root / ".env"
        load_dotenv(env_path)

    def get_db_config(self) -> DBConfig:
        """
        Build database configuration from environment variables.

        Environment variables are loaded from the configured
        .env file. Default fallback values are used when
        variables are not defined.

        Returns
        -------
        DBConfig
            Typed database configuration object.
        """

        return DBConfig(
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            database=os.getenv("MYSQL_DB", "nvidia_timeseries")
        )
