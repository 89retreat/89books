"""Prepares photos: upright, smaller and without EXIF metadata."""

import base64
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

MAX_SIDE = 1600


def prepare(path: Path) -> bytes:
    """JPEG bytes with rotation applied, at most MAX_SIDE pixels and no metadata."""
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image.thumbnail((MAX_SIDE, MAX_SIDE))
        buffer = BytesIO()
        image.save(buffer, "JPEG", quality=80, optimize=True)
    return buffer.getvalue()


def data_uri(jpeg: bytes) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(jpeg).decode()
