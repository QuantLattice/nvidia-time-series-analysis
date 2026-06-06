"""
Plot layer stack management.

This module provides a lightweight container for managing plot layers
within a plotting session.

The stack acts as an intermediate composition layer between:
- session orchestration (PlotSession);
- rendering backend (Renderer implementations).

It is responsible for:
- storing layers in insertion order;
- enforcing uniqueness of layers (by id if available);
- separating layers by placement type;
- providing query utilities for rendering pipelines.

Design principle
-----------------
The stack is intentionally framework-agnostic and does not perform any
rendering logic. It only organizes and indexes layers for downstream
consumption.
"""


from typing import (
    Iterable,
    List,
    Optional
)

from work.library.plotting.contracts import (
    LayerPlacement,
    PlotLayer
)


class LayerStack:
    """
    Container for plot layers used during rendering.

    The stack stores plot layers in insertion order and provides helper
    methods for grouping and querying layers by placement.

    Notes
    -----
    - The stack does not perform rendering.
    - It acts as a registry for PlotLayer objects.
    - Ordering is preserved for deterministic rendering.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        """
        Initialize an empty layer stack.
        """

        self._layers: List[PlotLayer] = []

    # ------------------------------------------------------------------
    # Layer management
    # ------------------------------------------------------------------

    def add_layer(
        self,
        layer: PlotLayer
    ) -> None:
        """
        Add a single plot layer to the stack.

        If a layer with the same identifier already exists, it is
        replaced to ensure uniqueness.

        Parameters
        ----------
        layer : PlotLayer
            Plot layer to append to the stack.

        Returns
        -------
        None
        """

        self.remove_by_id(layer_id=layer.id)

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
            Iterable of plot layers.

        Returns
        -------
        None
        """

        for layer in layers:
            self.add_layer(layer)

    def remove_layer(
        self,
        layer: PlotLayer
    ) -> bool:
        """
        Remove a layer instance from the stack.

        Parameters
        ----------
        layer : PlotLayer
            Layer to remove.

        Returns
        -------
        bool
            True if layer was removed, False otherwise.
        """

        return self.remove_by_id(layer.id)

    def remove_by_id(
        self,
        layer_id: str
    ) -> bool:
        """
        Remove a layer by its identifier.

        Parameters
        ----------
        layer_id : str
            Unique identifier of the layer.

        Returns
        -------
        bool
            True if a layer was removed, False otherwise.
        """

        for index, layer in enumerate(self._layers):
            if layer.id == layer_id:
                del self._layers[index]
                return True

        return False

    def clear(self) -> None:
        """
        Remove all layers from the stack.
        """

        self._layers.clear()

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
    # Collection protocol
    # ------------------------------------------------------------------

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
