"""Resolves reader-owned book covers at the local client boundary.

The reusable shelf core receives data URIs, never paths or image decoders. HTTPS covers stay remote;
local covers live under the shelf's covers/ directory so they cannot be mistaken for shelf photos.
"""

from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image, UnidentifiedImageError

from shelf import photos as photo_tools
from shelf.config import PHOTO_EXTENSIONS
from shelf.shelf_file import ShelfFile

MAX_BYTES = 5 * 1024 * 1024
MAX_PIXELS = 25_000_000
MAX_SIDE = 1000
COVERS_DIR = "covers"


class CoverAssetError(ValueError):
    """A book cover cannot be safely rendered from this shelf folder."""


def resolve_cover_assets(folder: Path, shelf: ShelfFile) -> dict[tuple[int, int], str]:
    """Returns sanitized data URIs for local covers and performs no network access."""
    folder = Path(folder)
    cover_root = (folder / COVERS_DIR).resolve()
    assets: dict[tuple[int, int], str] = {}
    for shelf_index, section in enumerate(shelf.shelves):
        for book_index, book in enumerate(section.books):
            cover = book.cover
            if cover is None or cover == "none":
                continue
            parsed = urlsplit(cover)
            if parsed.scheme or parsed.netloc:
                if parsed.scheme != "https" or not parsed.netloc:
                    raise _error(book.title, cover, "must be a complete HTTPS URL")
                continue

            relative = Path(cover)
            if relative.is_absolute() or not relative.parts or relative.parts[0] != COVERS_DIR:
                raise _error(
                    book.title,
                    cover,
                    f'must be HTTPS, "none", or a file inside {COVERS_DIR}/',
                )
            try:
                path = (folder / relative).resolve(strict=True)
            except (FileNotFoundError, OSError) as exc:
                raise _error(book.title, cover, "was not found") from exc
            if not path.is_relative_to(cover_root):
                raise _error(book.title, cover, f"is outside the {COVERS_DIR} folder")
            if not path.is_file():
                raise _error(book.title, cover, "is not a file")
            if path.suffix.lower() not in PHOTO_EXTENSIONS:
                raise _error(book.title, cover, "is not a supported image")
            if path.stat().st_size > MAX_BYTES:
                raise _error(book.title, cover, "is larger than 5 MiB")

            try:
                with Image.open(path) as image:
                    width, height = image.size
                if width * height > MAX_PIXELS:
                    raise _error(book.title, cover, "is larger than 25 megapixels")
                prepared = photo_tools.prepare(path, MAX_SIDE)
            except CoverAssetError:
                raise
            except (UnidentifiedImageError, OSError, ValueError) as exc:
                raise _error(book.title, cover, "could not be read as an image") from exc
            assets[(shelf_index, book_index)] = photo_tools.data_uri(prepared)
    return assets


def _error(title: str, cover: str, message: str) -> CoverAssetError:
    return CoverAssetError(f'Book "{title}": cover "{cover}" {message}.')
