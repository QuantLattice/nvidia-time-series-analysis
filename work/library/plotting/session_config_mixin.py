"""
Chart-configuration mixin for PlotSession.

Provides ``PlotSessionConfigMixin``, which groups all property
getters and setter helpers that delegate to ``self._chart_config``.

The concrete class must supply:
- ``self._chart_config`` — a ``ChartConfig`` instance;
- ``self._mark_dirty()`` — marks the session for re-rendering.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self


class PlotSessionConfigMixin:
    """
    Mixin that exposes chart-configuration getters and setters.

    All methods read from or write to ``self._chart_config`` and
    call ``self._mark_dirty()`` after every mutation.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    # ------------------------------------------------------------------
    # Setters — text labels
    # ------------------------------------------------------------------

    def set_title(self, value: str) -> "Self":
        """Set the chart title."""
        self._chart_config.title = value
        return self._mark_dirty()

    def set_xlabel(self, value: str) -> "Self":
        """Set the x-axis label."""
        self._chart_config.xlabel = value
        return self._mark_dirty()

    def set_primary_ylabel(self, value: str) -> "Self":
        """Set the primary y-axis label."""
        self._chart_config.primary_ylabel = value
        return self._mark_dirty()

    def set_overlay_ylabel(self, value: str) -> "Self":
        """Set the overlay y-axis label."""
        self._chart_config.overlay_ylabel = value
        return self._mark_dirty()

    # ------------------------------------------------------------------
    # Setters — visibility flags
    # ------------------------------------------------------------------

    def set_show_xlabel(self, value: bool) -> "Self":
        """Control visibility of the x-axis label."""
        self._chart_config.show_xlabel = value
        return self._mark_dirty()

    def set_show_primary_ylabel(self, value: bool) -> "Self":
        """Control visibility of the primary y-axis label."""
        self._chart_config.show_primary_ylabel = value
        return self._mark_dirty()

    def set_show_overlay_ylabel(self, value: bool) -> "Self":
        """Control visibility of the overlay y-axis label."""
        self._chart_config.show_overlay_ylabel = value
        return self._mark_dirty()

    def set_show_title(self, value: bool) -> "Self":
        """Control visibility of the chart title."""
        self._chart_config.show_title = value
        return self._mark_dirty()

    def set_show_xticks(self, value: bool) -> "Self":
        """Control visibility of x-axis tick labels."""
        self._chart_config.show_xticks = value
        return self._mark_dirty()

    def set_show_primary_yticks(self, value: bool) -> "Self":
        """Control visibility of primary y-axis tick labels."""
        self._chart_config.show_primary_yticks = value
        return self._mark_dirty()

    def set_show_overlay_yticks(self, value: bool) -> "Self":
        """Control visibility of overlay y-axis tick labels."""
        self._chart_config.show_overlay_yticks = value
        return self._mark_dirty()

    def set_show_grid(self, value: bool) -> "Self":
        """Control grid visibility."""
        self._chart_config.show_grid = value
        return self._mark_dirty()

    def set_show_legend(self, value: bool) -> "Self":
        """Control legend visibility."""
        self._chart_config.show_legend = value
        return self._mark_dirty()

    # ------------------------------------------------------------------
    # Properties — text labels
    # ------------------------------------------------------------------

    @property
    def title(self) -> Optional[str]:
        """Current chart title, or None if not set."""
        return self._chart_config.title

    @property
    def xlabel(self) -> Optional[str]:
        """Current x-axis label, or None if not set."""
        return self._chart_config.xlabel

    @property
    def primary_ylabel(self) -> Optional[str]:
        """Current primary y-axis label, or None if not set."""
        return self._chart_config.primary_ylabel

    @property
    def overlay_ylabel(self) -> Optional[str]:
        """Current overlay y-axis label, or None if not set."""
        return self._chart_config.overlay_ylabel

    # ------------------------------------------------------------------
    # Properties — visibility flags
    # ------------------------------------------------------------------

    @property
    def show_title(self) -> bool:
        """True if the chart title is displayed."""
        return self._chart_config.show_title

    @property
    def show_xlabel(self) -> bool:
        """True if the x-axis label is displayed."""
        return self._chart_config.show_xlabel

    @property
    def show_primary_ylabel(self) -> bool:
        """True if the primary y-axis label is displayed."""
        return self._chart_config.show_primary_ylabel

    @property
    def show_overlay_ylabel(self) -> bool:
        """True if the overlay y-axis label is displayed."""
        return self._chart_config.show_overlay_ylabel

    @property
    def show_xticks(self) -> bool:
        """True if x-axis tick labels are displayed."""
        return self._chart_config.show_xticks

    @property
    def show_primary_yticks(self) -> bool:
        """True if primary y-axis tick labels are displayed."""
        return self._chart_config.show_primary_yticks

    @property
    def show_overlay_yticks(self) -> bool:
        """True if overlay y-axis tick labels are displayed."""
        return self._chart_config.show_overlay_yticks

    @property
    def show_grid(self) -> bool:
        """True if chart grid lines are displayed."""
        return self._chart_config.show_grid

    @property
    def show_legend(self) -> bool:
        """True if the chart legend is displayed."""
        return self._chart_config.show_legend
