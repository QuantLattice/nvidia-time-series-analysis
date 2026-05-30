"""
Plot layer stack management.

This module provides a lightweight container for managing plot layers
within a plotting session.

The stack supports:
- adding individual layers;
- extending from iterables of layers;
- separating primary and overlay layers by placement;
- iteration and inspection utilities.
"""


from typing import Iterable, List

from work.library.plotting.contracts import (
    LayerPlacement,
    PlotLayer
)


class LayerStack:
    """
    Container for plot layers used during rendering.

    The stack stores plot layers in insertion order and provides helper
    methods for grouping layers by placement category.

    The class is intentionally minimal and acts as the session-level
    layer registry for the plotting subsystem.

    Notes
    -----
    The stack does not perform rendering itself. It only stores and
    organizes plot layers for later consumption by a renderer.
    """

    def __init__(self) -> None:
        """
        Initialize an empty plot layer stack.
        """

        self._layers: List[PlotLayer] = []

    def add_layer(
        self,
        layer: PlotLayer
    ) -> None:
        """
        Add a single plot layer to the stack.

        Parameters
        ----------
        layer : PlotLayer
            Plot layer to append.

        Returns
        -------
        None
            The layer is stored by side effect.
        """

        self._layers.append(layer)

    def extend(
        self,
        layers: Iterable[PlotLayer]
    ) -> None:
        """
        Add multiple plot layers to the stack.

        Parameters
        ----------
        layers : Iterable[PlotLayer]
            Iterable of plot layers to append.

        Returns
        -------
        None
            Layers are stored by side effect.
        """

        self._layers.extend(layers)

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

    def clear(self) -> None:
        """
        Remove all stored layers.

        Returns
        -------
        None
            The stack is cleared by side effect.
        """

        self._layers.clear()

    def __iter__(self):
        """
        Iterate over stored layers in insertion order.

        Returns
        -------
        Iterator[PlotLayer]
            Iterator over the internal layer sequence.
        """

        return iter(self._layers)

    def __len__(self):
        """
        Return the number of stored layers.

        Returns
        -------
        int
            Number of layers currently stored in the stack.
        """

        return len(self._layers)

    def __repr__(self):
        """
        Return a compact string representation of the stack.

        Returns
        -------
        str
            Human-readable representation of the layer stack.
        """

        return f"LayerStack(layers={len(self)})"

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
