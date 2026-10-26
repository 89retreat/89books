"""Checks that an Open Library cover image looks like a book cover.

Open Library sometimes stores a scan of the inside of a book as its cover: a table of contents, or two
open pages photographed sideways. Those scans are grey and mostly blank, or wider than tall, while real
covers carry colour. A rejected cover makes the book appear as a drawn spine.
"""

import json
from collections.abc import Callable
from io import BytesIO
from pathlib import Path

import httpx
from PIL import Image

from shelf.openlibrary import USER_AGENT

URL = "https://covers.openlibrary.org/b/id/{}-M.jpg?default=false"
MIN_HEIGHT_RATIO = 0.95  # covers are taller than wide; a square cover still passes
GREY = 1.0  # scans are stored in exact greys; printed covers keep a faint tint even when white
BLANK = 0.6  # share of near-white pixels in a scanned page


def looks_like_cover(jpeg: bytes) -> bool:
    with Image.open(BytesIO(jpeg)) as image:
        width, height = image.size
        if height / width < MIN_HEIGHT_RATIO:
            return False
        raw = image.convert("RGB").resize((40, 60)).tobytes()
    pixels = [raw[i : i + 3] for i in range(0, len(raw), 3)]
    spread = sum(max(p) - min(p) for p in pixels) / len(pixels)
    blank = sum(1 for p in pixels if min(p) > 200) / len(pixels)
    return not (spread < GREY and blank > BLANK)


def _fetch(cover_id: int) -> bytes:
    response = httpx.get(
        URL.format(cover_id), headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=30
    )
    response.raise_for_status()
    return response.content


class CoverCheck:
    """Remembers the verdict for each cover id, so each image is downloaded once."""

    def __init__(self, cache_path: Path, fetch: Callable[[int], bytes] = _fetch):
        self.cache_path = cache_path
        self.fetch = fetch
        self.cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}

    def ok(self, cover_id: int) -> bool:
        key = str(cover_id)
        if key not in self.cache:
            try:
                self.cache[key] = looks_like_cover(self.fetch(cover_id))
            except (OSError, httpx.HTTPError, ValueError):
                return True  # not cached: the page falls back to a spine if the image fails there too
        return self.cache[key]

    def save(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(self.cache, indent=1), encoding="utf-8")
