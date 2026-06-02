"""Unit tests for the CSV import pipeline.

These tests write real CSV files to disk, load them through ``CSVLoader``,
and run the extract -> map -> normalize -> validate stages against several
datasets:

- a well-formed CSV with standard headers;
- a well-formed CSV using alternative (aliased) headers;
- a CSV whose column names do not match any known alias;
- a CSV where the integer ``volume`` column is filled with fractional floats.

The goal is to confirm that valid files pass and that malformed files fail
with a clear error naming the offending column.
"""


import pandas as pd
import pytest

from work.library.io.csv_loader import CSVLoader
from work.scripts.contracts.schemas import StockQuoteSchema as S
from work.scripts.contracts.mappers import StockQuoteMapper
from work.scripts.contracts.validation import (
    StockQuoteNormalizer,
    StockQuoteValidator,
)


def _write_csv(tmp_path, name: str, content: str) -> str:
    """Write CSV ``content`` to ``tmp_path/name`` and return the path."""

    path = tmp_path / name
    path.write_text(content)
    return str(path)


def _run_pipeline(path: str) -> pd.DataFrame:
    """Run the full extract -> map -> normalize -> validate pipeline."""

    df = CSVLoader.load(path)
    df = StockQuoteMapper.map(df)
    df = StockQuoteNormalizer.normalize(df)
    StockQuoteValidator.validate(df)
    return df


# =========================================================
# VALID CSV - STANDARD HEADERS
# =========================================================

@pytest.mark.unit
def test_valid_csv_standard_headers(tmp_path) -> None:
    """A clean CSV with standard headers passes the whole pipeline."""

    path = _write_csv(
        tmp_path,
        "standard.csv",
        "date,open,high,low,close,volume\n"
        "2024-01-01,100,110,90,105,1000\n"
        "2024-01-02,106,112,95,108,2000\n",
    )

    df = _run_pipeline(path)

    assert len(df) == 2
    assert list(df.columns) == S.ALL_COLUMNS
    assert pd.api.types.is_datetime64_any_dtype(df[S.TRADE_DATE])
    assert pd.api.types.is_integer_dtype(df[S.VOLUME])
    assert df[S.TRADE_DATE].is_monotonic_increasing


# =========================================================
# VALID CSV - ALTERNATIVE (ALIASED) HEADERS
# =========================================================

@pytest.mark.unit
def test_valid_csv_alternative_headers(tmp_path) -> None:
    """A CSV using aliased headers is resolved to the internal schema."""

    path = _write_csv(
        tmp_path,
        "aliased.csv",
        "datetime,o,h,l,c,vol\n"
        "2024-03-10,50.5,55.0,48.0,52.0,300\n"
        "2024-03-11,52.0,58.0,51.0,57.0,450\n"
        "2024-03-12,57.0,60.0,55.0,59.0,500\n",
    )

    df = _run_pipeline(path)

    assert len(df) == 3
    assert list(df.columns) == S.ALL_COLUMNS
    assert pd.api.types.is_numeric_dtype(df[S.CLOSE_PRICE])
    assert pd.api.types.is_integer_dtype(df[S.VOLUME])


# =========================================================
# INVALID CSV - WRONG COLUMN NAMES
# =========================================================

@pytest.mark.unit
def test_csv_with_wrong_column_names(tmp_path) -> None:
    """A CSV with unrecognized headers fails, naming the missing column."""

    path = _write_csv(
        tmp_path,
        "wrong_headers.csv",
        "day,opening,top,bottom,closing,shares\n"
        "2024-01-01,100,110,90,105,1000\n",
    )

    # None of these headers match a known alias, so the mapper rejects the
    # file and reports the missing required columns by name.
    with pytest.raises(ValueError, match=r"Invalid CSV.*cannot map") as exc:
        _run_pipeline(path)

    # Every unmatched required column is listed, each with a fix hint.
    message = str(exc.value)
    for field in (
        S.TRADE_DATE, S.OPEN_PRICE, S.HIGH_PRICE,
        S.LOW_PRICE, S.CLOSE_PRICE, S.VOLUME,
    ):
        assert f"'{field}'" in message
    assert message.count("Fix: rename") == 6


@pytest.mark.unit
def test_csv_with_single_wrong_column_name(tmp_path) -> None:
    """Only the unmatched column is reported when the rest are valid."""

    path = _write_csv(
        tmp_path,
        "one_wrong_header.csv",
        # every header is valid except the volume column ('shares')
        "date,open,high,low,close,shares\n"
        "2024-01-01,100,110,90,105,1000\n",
    )

    with pytest.raises(ValueError, match=f"'{S.VOLUME}'"):
        _run_pipeline(path)


# =========================================================
# INVALID CSV - VOLUME FILLED WITH FLOATS
# =========================================================

@pytest.mark.unit
def test_csv_volume_filled_with_float(tmp_path) -> None:
    """Volume must be integer; fractional float values fail by column name."""

    path = _write_csv(
        tmp_path,
        "float_volume.csv",
        "date,open,high,low,close,volume\n"
        "2024-01-01,100,110,90,105,1000.5\n"
        "2024-01-02,106,112,95,108,2000.7\n",
    )

    with pytest.raises(ValueError, match=f"'{S.VOLUME}': contains non-integer values"):
        _run_pipeline(path)


# =========================================================
# INVALID CSV - MULTIPLE PROBLEMS AT ONCE
# =========================================================

@pytest.mark.unit
def test_csv_reports_all_bad_columns_together(tmp_path) -> None:
    """A single error lists every offending column and how to fix it.

    The file has two independent, distinct-column problems that both
    survive normalization:
    - a fractional ``volume`` value (must be a whole integer);
    - a row where ``high`` is below ``low``.
    """

    path = _write_csv(
        tmp_path,
        "many_problems.csv",
        "date,open,high,low,close,volume\n"
        "2024-01-01,100,80,90,85,1000.5\n"
        "2024-01-02,101,111,95,108,2000\n",
    )

    with pytest.raises(ValueError) as exc:
        _run_pipeline(path)

    message = str(exc.value)
    assert f"'{S.VOLUME}': contains non-integer values" in message
    assert f"'{S.HIGH_PRICE}': 1 row(s) have high < low" in message
    # Both problems are reported in a single failure, not one at a time.
    assert message.count("Fix:") == 2


@pytest.mark.unit
def test_csv_warns_about_dropped_rows(tmp_path) -> None:
    """Rows dropped for missing required values raise a warning naming them."""

    path = _write_csv(
        tmp_path,
        "dropped_rows.csv",
        "date,open,high,low,close,volume\n"
        "2024-01-01,100,110,90,105,1000\n"
        # 'open' is non-numeric -> coerced to NaN -> row dropped in normalize.
        "2024-01-02,oops,112,95,108,2000\n",
    )

    with pytest.warns(UserWarning, match=r"Dropped 1 row\(s\)"):
        df = _run_pipeline(path)

    # The valid row survives; the offending row is gone.
    assert len(df) == 1
    assert df[S.OPEN_PRICE].tolist() == [100]


@pytest.mark.unit
def test_csv_integer_valued_floats_are_accepted(tmp_path) -> None:
    """Integer-valued floats (e.g. 1000.0) are accepted and cast to Int64."""

    path = _write_csv(
        tmp_path,
        "intlike_volume.csv",
        "date,open,high,low,close,volume\n"
        "2024-01-01,100,110,90,105,1000.0\n"
        "2024-01-02,106,112,95,108,2000.0\n",
    )

    df = _run_pipeline(path)

    assert pd.api.types.is_integer_dtype(df[S.VOLUME])
    assert df[S.VOLUME].tolist() == [1000, 2000]
