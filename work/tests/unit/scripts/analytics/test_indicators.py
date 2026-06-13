"""Unit tests for technical indicator functions.

Covers: SMA, EMA, VWMA, returns (daily, log, cumulative),
and RSI (SMA and Wilder methods).
"""
import pytest
import pandas as pd
import numpy as np

from work.scripts.analytics.indicators.moving_averages import sma, ema, vwma
from work.scripts.analytics.indicators.returns import (
    daily_return,
    log_return,
    cumulative_return,
    rolling_return,
)
from work.scripts.analytics.indicators.rsi import rsi, RSIMethod

# ── common price series ───────────────────────────────────

PRICES = pd.Series(
    [100.0, 102.0, 101.0, 105.0, 107.0, 106.0, 108.0, 110.0, 109.0, 111.0]
)
VOLUME = pd.Series(
    [1000, 1200, 900, 1500, 1100, 800, 1300, 1600, 950, 1400],
    dtype=float,
)


# =========================================================
# SMA
# =========================================================

@pytest.mark.unit
def test_sma_length() -> None:
    """SMA output has the same length as input."""
    result = sma(PRICES, window=3)
    assert len(result) == len(PRICES)


@pytest.mark.unit
def test_sma_first_valid() -> None:
    """Third element of SMA(3) equals mean of first three prices."""
    result = sma(PRICES, window=3)
    expected = (100.0 + 102.0 + 101.0) / 3
    assert result.iloc[2] == pytest.approx(expected)


@pytest.mark.unit
def test_sma_leading_nans() -> None:
    """SMA(3) has NaN for the first window-1 positions."""
    result = sma(PRICES, window=3)
    assert pd.isna(result.iloc[0])
    assert pd.isna(result.iloc[1])
    assert not pd.isna(result.iloc[2])


@pytest.mark.unit
def test_sma_window_1_equals_input() -> None:
    """SMA(1) is identical to the input series."""
    result = sma(PRICES, window=1)
    pd.testing.assert_series_equal(
        result.reset_index(drop=True),
        PRICES.reset_index(drop=True),
    )


# =========================================================
# EMA
# =========================================================

@pytest.mark.unit
def test_ema_length() -> None:
    """EMA output has the same length as input."""
    assert len(ema(PRICES, window=3)) == len(PRICES)


@pytest.mark.unit
def test_ema_differs_from_sma() -> None:
    """EMA and SMA produce different values (EMA weights recent data more)."""
    result_ema = ema(PRICES, window=3).dropna()
    result_sma = sma(PRICES, window=3).dropna()
    assert not result_ema.equals(result_sma)


@pytest.mark.unit
def test_ema_monotone_on_rising_prices() -> None:
    """EMA is non-decreasing on a strictly rising price series."""
    rising = pd.Series([float(i) for i in range(1, 20)])
    result = ema(rising, window=5).dropna()
    diffs = result.diff().dropna()
    assert (diffs >= 0).all()


# =========================================================
# VWMA
# =========================================================

@pytest.mark.unit
def test_vwma_length() -> None:
    """VWMA output has the same length as price input."""
    assert len(vwma(PRICES, VOLUME, window=3)) == len(PRICES)


@pytest.mark.unit
def test_vwma_differs_from_sma() -> None:
    """VWMA and SMA differ when volumes are non-uniform."""
    v = vwma(PRICES, VOLUME, window=3).dropna()
    s = sma(PRICES, window=3).dropna()
    # They won't be equal because volumes differ
    assert not v.equals(s)


# =========================================================
# RETURNS
# =========================================================

@pytest.mark.unit
def test_daily_return_length() -> None:
    """daily_return has the same length as input (first value is NaN)."""
    result = daily_return(PRICES)
    assert len(result) == len(PRICES)


@pytest.mark.unit
def test_daily_return_first_nan() -> None:
    """First element of daily_return is NaN."""
    assert pd.isna(daily_return(PRICES).iloc[0])


@pytest.mark.unit
def test_daily_return_second_value() -> None:
    """Second daily return equals (102-100)/100 = 0.02."""
    result = daily_return(PRICES)
    assert result.iloc[1] == pytest.approx(0.02)


@pytest.mark.unit
def test_log_return_second_value() -> None:
    """Second log return equals ln(102/100)."""
    result = log_return(PRICES)
    assert result.iloc[1] == pytest.approx(np.log(102.0 / 100.0))


@pytest.mark.unit
def test_cumulative_return_starts_at_zero() -> None:
    """First cumulative return is 0 (no change at start)."""
    result = cumulative_return(PRICES)
    assert result.iloc[0] == pytest.approx(0.0)


@pytest.mark.unit
def test_cumulative_return_positive_on_rise() -> None:
    """Cumulative return is positive at end of rising series."""
    rising = pd.Series([100.0, 110.0, 121.0])
    result = cumulative_return(rising)
    assert result.iloc[-1] > 0


@pytest.mark.unit
def test_rolling_return_length() -> None:
    assert len(rolling_return(PRICES, window=3)) == len(PRICES)


# =========================================================
# RSI
# =========================================================

@pytest.mark.unit
def test_rsi_sma_range() -> None:
    """RSI values are in [0, 100]."""
    long_prices = pd.Series(
        [100.0 + i * 0.5 + (i % 3) * (-2.0) for i in range(30)]
    )
    result = rsi(long_prices, window=14, method=RSIMethod.SMA)
    valid = result.dropna()
    assert (valid >= 0).all()
    assert (valid <= 100).all()


@pytest.mark.unit
def test_rsi_wilder_range() -> None:
    """RSI (Wilder) values are in [0, 100]."""
    long_prices = pd.Series(
        [100.0 + i * 0.5 + (i % 3) * (-2.0) for i in range(30)]
    )
    result = rsi(long_prices, window=14, method=RSIMethod.WILDER)
    valid = result.dropna()
    assert (valid >= 0).all()
    assert (valid <= 100).all()


@pytest.mark.unit
def test_rsi_constant_series_is_nan_or_50() -> None:
    """RSI on constant prices is NaN or 50 (no gain/loss)."""
    constant = pd.Series([100.0] * 20)
    result = rsi(constant, window=14, method=RSIMethod.SMA)
    valid = result.dropna()
    # All gains and losses are 0; RSI is undefined (NaN) or 50
    assert valid.empty or (valid == pytest.approx(50.0)).all()


@pytest.mark.unit
def test_rsi_rising_trend_above_50() -> None:
    """RSI on a consistently rising series should be above 50."""
    rising = pd.Series([float(i) for i in range(1, 40)])
    result = rsi(rising, window=14, method=RSIMethod.WILDER)
    valid = result.dropna()
    assert (valid > 50).all()
