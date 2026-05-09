"""
Image loading and processing utilities for GUI components.

This module provides a unified interface for:
- loading images from disk
- resizing and preprocessing
- converting images to Tkinter-compatible formats
- applying simple color transformations
"""


from PIL import (
    Image,
    ImageTk,
    ImageFilter
)
from pathlib import Path
from typing import (
    Tuple,
    Optional,
    Union
)


class ImageLoader:
    """
    Utility class for image loading and processing.

    Supports:
    - base path resolution
    - default image sizing
    - resizing with LANCZOS filter
    - image tinting
    - conversion to Tkinter PhotoImage

    Parameters
    ----------
    base_path : Union[str, Path]
        Root directory for image resources.

    default_size : Optional[Union[int, Tuple[int, int]]], optional
        Default size applied when loading images.
        If int is provided, square size is assumed.
    """

    def __init__(
        self,
        base_path: Union[str, Path],
        default_size: Optional[Union[int, Tuple[int, int]]] = None,
    ) -> None:
        """
        Initialize ImageLoader with base directory and optional default size.

        Parameters
        ----------
        base_path : Union[str, Path]
            Root directory where image assets are stored.

        default_size : Optional[Union[int, Tuple[int, int]]], optional
            Default size applied when loading images.
            If int is provided, image is treated as square (size x size).
            If None, size must be specified explicitly in `load` calls.

        Notes
        -----
        The loader does not validate existence of base_path at initialization
        to avoid unnecessary filesystem overhead. Validation is performed
        during image loading.
        """

        self.base_path = base_path

        self.default_size: Optional[Tuple[int, int]] = None
        if default_size is not None:
            self.default_size = self._normalize_size(size=default_size)

    def set_default_size(
        self,
        size: Union[int, Tuple[int, int]]
    ) -> None:
        """
        Set default image size.

        Parameters
        ----------
        size : Union[int, Tuple[int, int]]
            New default size for image resizing.
        """

        self.default_size = self._normalize_size(size=size)

    def load(
        self,
        rel_path: str,
        size: Optional[Union[int, Tuple[int, int]]] = None
    ) -> Image.Image:
        """
        Load and preprocess an image from disk.

        Steps:
        - open image from base path
        - convert to RGBA
        - resize using LANCZOS filter
        - apply sharpening filter

        Parameters
        ----------
        rel_path : str
            Relative path to image inside base directory.

        size : Optional[Union[int, Tuple[int, int]]], optional
            Target image size. If None, default_size is used.

        Returns
        -------
        Image.Image
            Processed PIL image.
        """

        image_path = Path(self.base_path) / rel_path
        image = Image.open(fp=image_path).convert(mode="RGBA")

        image = image.resize(
            size=self._normalize_size(size),
            resample=Image.Resampling.LANCZOS)
        image = image.filter(filter=ImageFilter.SHARPEN)

        return image

    def tint_image(
        self,
        image: Image.Image,
        color: str,
    ) -> Image.Image:
        """
        Apply color tint to an image while preserving alpha channel.

        Parameters
        ----------
        image : Image.Image
            Source image.

        color : str
            Hex color string (e.g. "#RRGGBB").

        Returns
        -------
        Image.Image
            Tinted image.
        """

        rgb = self._hex_to_rgb(color=color)

        _, _, _, a = image.split()

        solid_color = Image.new(
            mode="RGBA",
            size=image.size,
            color=rgb + (255,)
        )

        return Image.composite(image1=solid_color, image2=image, mask=a)

    def to_photo(self, image: Image.Image) -> ImageTk.PhotoImage:
        """
        Convert PIL image to Tkinter PhotoImage.

        Parameters
        ----------
        image : Image.Image
            PIL image.

        Returns
        -------
        ImageTk.PhotoImage
            Tkinter-compatible image object.
        """

        return ImageTk.PhotoImage(image=image)

    def _normalize_size(
        self,
        size: Optional[Union[int, Tuple[int, int]]],
    ) -> Tuple[int, int]:
        """
        Normalize image size into (width, height) tuple.

        Parameters
        ----------
        size : Optional[Union[int, Tuple[int, int]]]
            Input size specification.

        Returns
        -------
        tuple[int, int]
            Normalized size.

        Raises
        ------
        ValueError
            If neither size nor default_size is defined.
        """

        if size is None:
            if self.default_size is not None:
                if isinstance(self.default_size, int):
                    return (self.default_size, self.default_size)
                else:
                    return self.default_size
            else:
                raise ValueError(
                    "Image size is not defined "
                    "(neither size nor default_size)."
                )
        else:
            if isinstance(size, int):
                return (size, size)

            return size

    def _hex_to_rgb(self, color: str) -> Tuple[int, int, int]:
        """
        Convert hex color string to RGB tuple.

        Parameters
        ----------
        color : str
            Hex color in format "#RRGGBB".

        Returns
        -------
        Tuple[int, int, int]
            RGB color components.
        """

        color = color.lstrip("#")
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        return (r, g, b)
