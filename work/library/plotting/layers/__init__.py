"""
Plot layer implementations.

This package contains concrete and reusable plot layer base classes
used by the layered plotting subsystem.

Layers in this package implement the shared plot layer contract and
provide composable rendering behavior for primary and overlay content.
"""


from .base import (
    BaseLayer
)


__all__ = [
    "BaseLayer"
]
