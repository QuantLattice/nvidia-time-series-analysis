"""
Base forecasting model interface.

This module defines the abstract forecasting API shared by all model
implementations in the forecasting subsystem.

The base class provides:
- fit/predict contract definition;
- fit-state tracking;
- prediction argument validation.

Concrete forecasting models should inherit from this class and
implement the ``fit`` and ``predict`` methods.
"""


from abc import ABC, abstractmethod
import pandas as pd


class BaseForecast(ABC):
    """
    Abstract base class for forecasting models.

    This class defines the common interface and validation logic used by
    all forecasting model implementations.

    Subclasses must implement:
    - ``fit`` for model training;
    - ``predict`` for forecasting future values.

    Notes
    -----
    The class tracks whether a model has been fitted before allowing
    prediction calls.
    """

    def __init__(self) -> None:
        """
        Initialize the forecasting model state.

        The model starts in an unfitted state and must be trained before
        predictions can be generated.
        """

        self._is_fitted = False

    @abstractmethod
    def fit(
        self,
        series: pd.Series
    ) -> None:
        """
        Fit the forecasting model to a time series.

        Parameters
        ----------
        series : pd.Series
            Input training series.

        Raises
        ------
        NotImplementedError
            Must be implemented by subclasses.
        """

        ...

    @abstractmethod
    def predict(
        self,
        steps: int
    ) -> pd.Series:
        """
        Generate future values using the fitted model.

        Parameters
        ----------
        steps : int
            Number of future time steps to predict.

        Returns
        -------
        pd.Series
            Forecasted values.

        Raises
        ------
        NotImplementedError
            Must be implemented by subclasses.
        """

        ...

    def _validate_predict(
        self,
        steps: int
    ) -> None:
        """
        Validate prediction preconditions.

        Parameters
        ----------
        steps : int
            Number of forecast steps.

        Raises
        ------
        RuntimeError
            If the model has not been fitted.

        ValueError
            If ``steps`` is not a positive integer.
        """

        self._validate_is_fitted()
        self._validate_steps(steps=steps)

    def _validate_is_fitted(self) -> None:
        """
        Ensure that the model has been fitted before prediction.

        Raises
        ------
        RuntimeError
            If the model is not fitted.
        """

        if not self._is_fitted:
            raise RuntimeError(
                "Model must be fitted before prediction."
            )

    def _validate_steps(
        self,
        steps: int
    ) -> None:
        """
        Validate the forecast horizon.

        Parameters
        ----------
        steps : int
            Number of future time steps.

        Raises
        ------
        ValueError
            If ``steps`` is less than or equal to zero.
        """

        if steps <= 0:
            raise ValueError(
                "steps must be greater than 0."
            )
