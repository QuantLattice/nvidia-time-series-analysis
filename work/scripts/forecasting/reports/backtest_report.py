"""
Forecasting backtest report utilities.

This module provides a high-level orchestrator for chronological
train/test evaluation of forecasting models.

The report includes:
- train/test split metadata;
- fitted model predictions;
- aligned actual observations;
- standard error metrics.

The implementation is intended for:
- forecasting validation;
- benchmark comparison;
- model selection;
- quantitative backtesting workflows.
"""


from dataclasses import dataclass
import pandas as pd

from work.scripts.forecasting.constants import (
    DEFAULT_TEST_RATIO,
    DEFAULT_FORECAST_SERIES_NAME
)
from work.scripts.forecasting.evaluation import (
    mae,
    mse,
    rmse,
    mape,
    chronological_split,
)
from work.scripts.forecasting.factories import ForecastModelFactory
from work.scripts.forecasting.contracts import ForecastModelConfig


# ==========================================
# DTO: METRICS
# ==========================================

@dataclass(frozen=True)
class ForecastMetrics:
    """
    Standard forecasting error metrics.

    Attributes
    ----------
    mae : float
        Mean Absolute Error.

    mse : float
        Mean Squared Error.

    rmse : float
        Root Mean Squared Error.

    mape : float
        Mean Absolute Percentage Error.
    """

    mae: float
    mse: float
    rmse: float
    mape: float


# ==========================================
# DTO: REPORT RESULT
# ==========================================

@dataclass(frozen=True)
class BacktestReportResult:
    """
    Structured result of a forecasting backtest.

    Attributes
    ----------
    train_size : int
        Number of observations used for model fitting.

    test_size : int
        Number of observations used for evaluation.

    predictions : pd.Series
        Forecasted values aligned to the test index.

    actual : pd.Series
        Ground truth test values.

    metrics : ForecastMetrics
        Evaluation metrics computed from actual and predicted values.

    model_config : ForecastModelConfig
        Forecast model configuration used for backtesting.
    """

    train_size: int
    test_size: int

    predictions: pd.Series
    actual: pd.Series

    metrics: ForecastMetrics

    model_config: ForecastModelConfig


# ==========================================
# ORCHESTRATOR
# ==========================================

class BacktestReport:
    """
    High-level backtest report generator.

    This class performs chronological train/test evaluation of a forecasting
    model and returns a structured result object with predictions and metrics.

    The workflow includes:
    - chronological splitting of the input series;
    - model construction from configuration;
    - model fitting on the training subset;
    - prediction on the test horizon;
    - computation of standard error metrics;
    - packaging of the final report.
    """

    def generate(
        self,
        series: pd.Series,
        config: ForecastModelConfig,
        test_ratio: float = DEFAULT_TEST_RATIO
    ) -> BacktestReportResult:
        """
        Generate a backtest report for a time series.

        Parameters
        ----------
        series : pd.Series
            Input historical time series.

        config : ForecastModelConfig
            Forecast model configuration used for training and prediction.

        test_ratio : float, default=DEFAULT_TEST_RATIO
            Fraction of the series reserved for testing.

        Returns
        -------
        BacktestReportResult
            Structured backtest report containing train/test metadata,
            aligned predictions, actual values, and evaluation metrics.

        Raises
        ------
        ValueError
            If the input series is empty or the chronological split is invalid.

        Notes
        -----
        The split is chronological and preserves temporal ordering.
        No shuffling is performed.
        """

        if series.empty:
            raise ValueError("Input series is empty.")

        # =========================
        # 1. SPLIT
        # =========================
        split = chronological_split(
            series=series,
            test_ratio=test_ratio
        )

        train = split.train
        test = split.test

        if train.empty or test.empty:
            raise ValueError(
                "Train or test split is empty. "
                "Check the input series length and test_ratio."
            )

        # =========================
        # 2. MODEL
        # =========================
        model = ForecastModelFactory.create(
            config=config
        )
        model.fit(train)

        predictions = model.predict(steps=len(test))
        predictions = predictions.copy()
        predictions.index = test.index
        predictions.name = test.name or DEFAULT_FORECAST_SERIES_NAME

        actual = test.copy()

        # =========================
        # 3. METRICS
        # =========================
        metrics = ForecastMetrics(
            mae=mae(actual, predictions),
            mse=mse(actual, predictions),
            rmse=rmse(actual, predictions),
            mape=mape(actual, predictions),
        )

        # =========================
        # 4. REPORT BUILD
        # =========================
        return BacktestReportResult(
            train_size=len(train),
            test_size=len(test),
            predictions=predictions,
            actual=actual,
            metrics=metrics,
            model_config=config
        )
