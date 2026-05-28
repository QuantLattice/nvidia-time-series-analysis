"""
Forecast generation report utilities.

This module provides a high-level orchestrator that fits a forecasting
model, generates future predictions, and returns a structured report.

The report includes:
- history size;
- forecast horizon;
- predicted values;
- model configuration used for generation.

The implementation is intended for:
- direct forecasting workflows;
- GUI presentation layers;
- export and serialization pipelines.
"""


from dataclasses import dataclass
import pandas as pd

from work.scripts.forecasting.contracts import ForecastModelConfig
from work.scripts.forecasting.constants import (
    DEFAULT_FORECAST_HORIZON,
    DEFAULT_FORECAST_SERIES_NAME,
)
from work.scripts.forecasting.factories import ForecastModelFactory


@dataclass(frozen=True)
class ForecastReportResult:
    """
    Structured result of a forecast generation run.

    Attributes
    ----------
    history_size : int
        Number of observations used as historical input.

    forecast_horizon : int
        Number of future steps requested from the model.

    predictions : pd.Series
        Forecasted values with a generated future index.

    model_config : ForecastModelConfig
        Forecast model configuration used for generation.
    """

    history_size: int
    forecast_horizon: int

    predictions: pd.Series

    model_config: ForecastModelConfig


class ForecastReport:
    """
    High-level forecast report generator.

    This class orchestrates model construction, fitting, forecasting,
    and future index generation into a single report object.

    The report workflow includes:
    - model instantiation from configuration;
    - model fitting on the input series;
    - forecast generation;
    - future index construction;
    - packaging of the final structured result.
    """

    def generate(
        self,
        series: pd.Series,
        config: ForecastModelConfig,
        horizon: int = DEFAULT_FORECAST_HORIZON
    ) -> ForecastReportResult:
        """
        Generate a forecast report for a time series.

        Parameters
        ----------
        series : pd.Series
            Historical input time series used for fitting the model.

        config : ForecastModelConfig
            Forecast model configuration used to construct the model.

        horizon : int, default=DEFAULT_FORECAST_HORIZON
            Number of future steps to predict.

        Returns
        -------
        ForecastReportResult
            Structured forecast report containing predictions and metadata.

        Raises
        ------
        ValueError
            If the input series is empty or the forecast horizon is invalid.

        Notes
        -----
        The resulting forecast is reindexed using a generated future index
        when the input series has a supported index type.
        """

        if series.empty:
            raise ValueError("Input series is empty.")

        if horizon <= 0:
            raise ValueError("forecast_horizon must be greater than zero.")

        # =========================
        # 1. MODEL
        # =========================
        model = ForecastModelFactory.create(
            config=config
        )
        model.fit(series)

        # =========================
        # 2. PREDICTION
        # =========================
        predictions = model.predict(steps=horizon)
        predictions = predictions.copy()
        predictions.index = self._build_future_index(series, horizon)
        predictions.name = DEFAULT_FORECAST_SERIES_NAME

        # =========================
        # 3. REPORT BUILD
        # =========================
        return ForecastReportResult(
            history_size=len(series),
            forecast_horizon=horizon,
            predictions=predictions,
            model_config=config
        )

    def _build_future_index(
        self,
        series: pd.Series,
        horizon: int
    ) -> pd.Index:
        """
        Build a future index for forecasted values.

        Parameters
        ----------
        series : pd.Series
            Historical input series used as a reference for index generation.

        horizon : int
            Number of future time steps.

        Returns
        -------
        pd.Index
            Generated index suitable for forecast output.

        Raises
        ------
        ValueError
            If the forecast horizon is invalid.

        Notes
        -----
        The method attempts to preserve temporal structure when possible:

        - ``DatetimeIndex`` -> future date range with inferred frequency;
        - ``RangeIndex`` -> continuation of the numeric index;
        - fallback -> simple zero-based ``RangeIndex``.
        """

        if horizon <= 0:
            raise ValueError("forecast_horizon must be greater than zero.")

        index = series.index

        # =========================
        # DatetimeIndex case
        # =========================
        if isinstance(index, pd.DatetimeIndex) and len(index) > 0:
            freq = pd.infer_freq(index)

            if freq is not None:
                start = index[-1] + pd.tseries.frequencies.to_offset(freq)
                return pd.date_range(
                    start=start,
                    periods=horizon,
                    freq=freq
                )

        # =========================
        # RangeIndex case
        # =========================
        if isinstance(index, pd.RangeIndex) and len(index) > 0:
            step = index.step or 1
            start = index[-1] + step

            return pd.RangeIndex(
                start=start,
                stop=start + horizon * step,
                step=step
            )

        # =========================
        # Fallback
        # =========================
        return pd.RangeIndex(start=0, stop=horizon)
