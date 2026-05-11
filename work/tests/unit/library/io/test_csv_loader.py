"""Unit tests for CSVLoader.

Test coverage includes:
- valid CSV file returns a pandas DataFrame
- missing file raises FileNotFoundError
- empty file raises EmptyDataError (no validation — intentional design)
- wrong encoding raises UnicodeDecodeError
- loader does NOT validate or transform data (intentional delegation)
"""

import pytest
import pandas as pd
from pathlib import Path

from work.library.io.csv_loader import CSVLoader


def _write_csv(tmp_path: Path, content: str, name: str = "data.csv") -> str:
    csv_file = tmp_path / name
    csv_file.write_text(content, encoding="utf-8")
    return str(csv_file)


# =========================================================
# POSITIVE CASE
# =========================================================

@pytest.mark.unit
def test_load_valid_csv_returns_dataframe(tmp_path: Path) -> None:
    """Valid CSV file is loaded into a DataFrame with correct shape."""

    path = _write_csv(tmp_path, "a,b,c\n1,2,3\n4,5,6\n")

    df = CSVLoader.load(path)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["a", "b", "c"]
    assert len(df) == 2


@pytest.mark.unit
def test_load_single_row(tmp_path: Path) -> None:
    """CSV with a single data row returns a one-row DataFrame."""

    path = _write_csv(tmp_path, "x,y\n10,20\n")

    df = CSVLoader.load(path)

    assert len(df) == 1
    assert df["x"].iloc[0] == 10


# =========================================================
# MISSING FILE
# =========================================================

@pytest.mark.unit
def test_missing_file_raises(tmp_path: Path) -> None:
    """Non-existent path raises FileNotFoundError."""

    with pytest.raises(FileNotFoundError):
        CSVLoader.load(str(tmp_path / "missing.csv"))


# =========================================================
# EMPTY FILE
# =========================================================

@pytest.mark.unit
def test_empty_file_raises(tmp_path: Path) -> None:
    """Completely empty file raises pandas EmptyDataError."""

    path = _write_csv(tmp_path, "")

    with pytest.raises(pd.errors.EmptyDataError):
        CSVLoader.load(path)


# =========================================================
# ENCODING
# =========================================================

@pytest.mark.unit
def test_wrong_encoding_raises(tmp_path: Path) -> None:
    """File written in latin-1 with non-ASCII chars raises UnicodeDecodeError."""

    csv_file = tmp_path / "latin.csv"
    csv_file.write_bytes(b"name\ncaf\xe9\n")  # 'café' in latin-1 bytes

    with pytest.raises(UnicodeDecodeError):
        CSVLoader.load(str(csv_file))


# =========================================================
# NO VALIDATION
# =========================================================

@pytest.mark.unit
def test_loader_does_not_validate_data(tmp_path: Path) -> None:
    """Loader returns raw data without raising on invalid values."""

    path = _write_csv(tmp_path, "price,volume\nabc,xyz\n")

    df = CSVLoader.load(path)

    assert df["price"].iloc[0] == "abc"
    assert df["volume"].iloc[0] == "xyz"
