"""
Query mixin for the plot layer stack.

This module provides ``LayerStackQueryMixin``, a mixin class that
adds read-only query methods to a layer container.  The concrete
class must expose a ``_layers`` attribute (a ``List[PlotLayer]``)
for the mixin methods to operate on.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from typing import List, Optional

from work.library.plotting.contracts import (
    LayerPlacement,
    PlotLayer,
)


class LayerStackQueryMixin:
    """
    Read-only query helpers for a plot layer collection.

    This mixin expects the host class to define::

        self._layers: List[PlotLayer]

    It provides filtering and lookup utilities consumed by rendering
    pipelines without modifying the underlying collection.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        layer_id: str
    ) -> Optional[PlotLayer]:
        """
        Retrieve a layer by its identifier.

        Parameters
        ----------
        layer_id : str
            Layer identifier.

        Returns
        -------
        Optional[PlotLayer]
            Matching layer or None if not found.
        """

        for layer in self._layers:
            if layer.id == layer_id:
                return layer

        return None

    def get_all(self) -> List[PlotLayer]:
        """
        Return all stored plot layers.

        Returns
        -------
        List[PlotLayer]
            Copy of the internal layer list in insertion order.
        """

        return list(self._layers)

    def primary_layers(self) -> List[PlotLayer]:
        """
        Return plot layers marked as primary.

        Returns
        -------
        List[PlotLayer]
            Layers whose placement is ``LayerPlacement.PRIMARY``.
        """

        return self._get_layers_by_placement(
            placement=LayerPlacement.PRIMARY
        )

    def overlay_layers(self) -> List[PlotLayer]:
        """
        Return plot layers marked as overlay.

        Returns
        -------
        List[PlotLayer]
            Layers whose placement is ``LayerPlacement.OVERLAY``.
        """

        return self._get_layers_by_placement(
            placement=LayerPlacement.OVERLAY
        )

    def has_overlay_layers(self) -> bool:
        """
        Check whether overlay layers exist.

        Returns
        -------
        bool
            True if overlay layers are present.
        """

        return len(self.overlay_layers()) > 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_layers_by_placement(
        self,
        placement: LayerPlacement
    ) -> List[PlotLayer]:
        """
        Return layers matching a given placement.

        Parameters
        ----------
        placement : LayerPlacement
            Requested layer placement category.

        Returns
        -------
        List[PlotLayer]
            Layers whose placement matches the requested category.
        """

        return [
            layer
            for layer in self._layers
            if layer.placement == placement
        ]
