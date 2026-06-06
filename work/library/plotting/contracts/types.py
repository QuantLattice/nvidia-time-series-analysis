"""
Literal type definitions for plotting system configuration.

This module defines strongly-typed string and value constraints
used across the rendering and styling system.

These types act as contracts for Matplotlib-compatible styling
options and ensure consistency across rendering backends.
"""

from typing import Literal, TypeAlias


LineStyleLiteral: TypeAlias = Literal[
    "-", "solid",
    "--", "dashed",
    "-.", "dashdot",
    ":", "dotted",
    "none", "None", " ", ""
]
"""
Supported line style identifiers for line-based plot rendering.

These values map directly to Matplotlib line style specifications.
"""


MarkerStyle: TypeAlias = Literal[
    ".", ",",
    "o",
    "v", "^", "<", ">",
    "1", "2", "3", "4",
    "8", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D", "d", "|", "_",
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
    "none", "None", "", " "
]
"""
Supported marker style identifiers for scatter and line plots.

These values correspond to Matplotlib marker specifications.
"""


HatchStyle: TypeAlias = Literal[
    "/", "\\", "|", "-", "+", "X", "o", "O", ".", "*"
]
"""
Supported hatch pattern styles for filled plot areas.

Used for bar plots, histograms, and filled regions.
"""
