"""Prepares photos: upright, smaller and without EXIF metadata."""

import base64
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

MAX_SIDE = 1600  # sent to the model, which needs to read the spines
PAGE_SIDE = 1000  # embedded in the page


def prepare(path: Path, max_side: int = MAX_SIDE) -> bytes:
    """JPEG bytes with rotation applied, at most max_side pixels and no metadata."""
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image.thumbnail((max_side, max_side))
        buffer = BytesIO()
        image.save(buffer, "JPEG", quality=80, optimize=True)
    return buffer.getvalue()


def data_uri(jpeg: bytes) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(jpeg).decode()
