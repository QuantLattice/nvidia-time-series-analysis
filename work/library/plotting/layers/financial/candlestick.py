"""
Candlestick layer implementation.

This module defines the concrete layer used to render financial
candlestick charts on a Matplotlib axes object.

The layer supports OHLC data, configurable candle body styling,
wick styling, and automatic date-axis formatting.
"""


from typing import (
    Sequence,
    Optional,
    Any
)
import matplotlib.dates as mdates
import numpy as np
from numpy.typing import NDArray
from matplotlib.axes import Axes

from work.library.plotting.layers.base.layer import BaseLayer
from work.library.plotting.contracts.layer import LayerPlacement
from work.library.plotting.contracts.layer_style import CandlestickStyle


class CandlestickLayer(BaseLayer):
    """
    Renderable layer for financial candlestick charts.

    A candlestick layer visualizes open-high-low-close (OHLC) data
    as a sequence of candles with wicks and directional body styling.

    Parameters
    ----------
    x : Sequence[Any]
        X-axis coordinates for each candlestick. These are typically
        date-like values.

    open : Sequence[float]
        Opening values for each candle.

    high : Sequence[float]
        High values for each candle.

    low : Sequence[float]
        Low values for each candle.

    close : Sequence[float]
        Closing values for each candle.

    style : Optional[CandlestickStyle], default=None
        Visual styling configuration for the candlestick layer.

    placement : LayerPlacement, default=LayerPlacement.PRIMARY
        Rendering placement of the layer.

    width : Optional[float], default=None
        Width of each candle body.

    Notes
    -----
    The input series are converted to NumPy arrays for vectorized
    rendering. X-axis tick formatting is configured automatically for
    date-like values.
    """

    # ------------------------------------------------------------------
    # Matplotlib defaults
    # ------------------------------------------------------------------

    _WIDTH = 0.0

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        x: Sequence[Any],
        open: Sequence[float],
        high: Sequence[float],
        low: Sequence[float],
        close: Sequence[float],
        style: Optional[CandlestickStyle] = None,
        placement: LayerPlacement = LayerPlacement.PRIMARY,
        width: Optional[float] = None
    ) -> None:
        """
        Initialize a candlestick layer.

        Parameters
        ----------
        x : Sequence[Any]
            X-axis coordinates for each candlestick. These are typically
            date-like values.

        open : Sequence[float]
            Opening values for each candle.

        high : Sequence[float]
            High values for each candle.

        low : Sequence[float]
            Low values for each candle.

        close : Sequence[float]
            Closing values for each candle.

        style : Optional[CandlestickStyle], default=None
            Visual styling configuration for the candlestick layer.

        placement : LayerPlacement, default=LayerPlacement.PRIMARY
            Rendering placement of the layer.

        width : Optional[float], default=None
            Width of each candle body.
        """

        super().__init__(placement)

        self._x = list(x)
        self._open = np.asarray(open, dtype=float)
        self._high = np.asarray(high, dtype=float)
        self._low = np.asarray(low, dtype=float)
        self._close = np.asarray(close, dtype=float)

        self._style = style or CandlestickStyle()
        self._width = width or self._WIDTH

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def x(self) -> Sequence[Any]:
        """
        X-axis coordinates for the candlesticks.

        Returns
        -------
        Sequence[Any]
            Stored x-values used during rendering.
        """
        return self._x

    @property
    def open(self) -> NDArray[Any]:
        """
        Opening values for the candlesticks.

        Returns
        -------
        NDArray[Any]
            Stored open values used during rendering.
        """
        return self._open

    @property
    def high(self) -> NDArray[Any]:
        """
        High values for the candlesticks.

        Returns
        -------
        NDArray[Any]
            Stored high values used during rendering.
        """
        return self._high

    @property
    def low(self) -> NDArray[Any]:
        """
        Low values for the candlesticks.

        Returns
        -------
        NDArray[Any]
            Stored low values used during rendering.
        """
        return self._low

    @property
    def close(self) -> NDArray[Any]:
        """
        Closing values for the candlesticks.

        Returns
        -------
        NDArray[Any]
            Stored close values used during rendering.
        """
        return self._close

    @property
    def style(self) -> CandlestickStyle:
        """
        Visual style of the candlestick layer.

        Returns
        -------
        CandlestickStyle
            Styling configuration used for rendering.
        """
        return self._style

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, axes: Axes) -> None:
        """
        Render the candlestick layer on a Matplotlib axes.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing.

        Notes
        -----
        Rendering is performed as a side effect on the provided axes.
        The x-axis is formatted as dates after the candles are drawn.
        """

        x = np.asarray(self._x)
        o = self._open
        h = self._high
        lo = self._low
        c = self._close

        style = self.style
        width = self._width

        linestyle = style.linestyle or "solid"

        # 1. WICKS

        axes.vlines(  # type: ignore
            x=x,
            ymin=lo,
            ymax=h,
            color=style.wick_color,
            linestyles=linestyle,
            linewidth=style.wick_linewidth,
            alpha=style.wick_alpha,
            zorder=style.zorder,
        )

        # 2. SPLIT BULL / BEAR (vectorized mask)

        up_mask = c >= o
        down_mask = ~up_mask

        # 3. BULLISH CANDLES

        if np.any(up_mask):
            axes.bar(  # type: ignore
                x=x[up_mask],
                height=(c - o)[up_mask],
                bottom=o[up_mask],
                width=width,
                color=style.up_color,
                alpha=style.body_alpha,
                linewidth=style.edge_linewidth,
                edgecolor=style.edgecolor,
                hatch=style.hatch,
                zorder=style.zorder,
            )

        # 4. BEARISH CANDLES

        if np.any(down_mask):
            axes.bar(  # type: ignore
                x=x[down_mask],
                height=(o - c)[down_mask],
                bottom=c[down_mask],
                width=width,
                color=style.down_color,
                alpha=style.body_alpha,
                linewidth=style.edge_linewidth,
                edgecolor=style.edgecolor,
                hatch=style.hatch,
                zorder=style.zorder,
            )

        # 5. X-axis formatting (dates)

        axes.xaxis.set_major_locator(mdates.AutoDateLocator())
        axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        axes.tick_params(axis="x")  # type: ignore
