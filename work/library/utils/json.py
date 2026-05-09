"""
JSON file utilities for reading and writing structured data.

This module provides lightweight wrappers over Python's built-in
json module with consistent error handling and Path support.
"""


import json
from pathlib import Path
from typing import (
    Any,
    Dict,
    Union
)


def load(path: Union[Path, str]) -> Dict[Any, Any]:
    """
    Load JSON data from a file.

    Parameters
    ----------
    path : Union[Path, str]
        Path to the JSON file.

    Returns
    -------
    Dict[Any, Any]
        Parsed JSON data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with path.open(mode="r", encoding="utf-8") as f:
        return json.load(fp=f)


def save(path: Union[Path, str], data: Dict[Any, Any]) -> None:
    """
    Save data to a JSON file.

    Parameters
    ----------
    path : Union[Path, str]
        Output file path.

    data : Dict[Any, Any]
        Data to serialize into JSON.
    """

    path = Path(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj=data, fp=f, ensure_ascii=False, indent=2)
