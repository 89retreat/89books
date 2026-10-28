"""Renders the shelf page: photo mosaic, lens and the portrait themes as shelves."""

import base64
import re
from collections.abc import Mapping
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

from shelf.shelf_file import ShelfFile
from shelf.shelves import build_shelves, frequent_authors, mosaic, shelves_from_file

TEMPLATES = Path(__file__).parent / "templates"
TITLE_FONT = Path(__file__).parent / "fonts" / "newsreader-italic-500-latin.woff2"


def emphasize(text: str) -> Markup:
    """Escapes text, then turns *Book Title* into <em>Book Title</em>."""
    return Markup(re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", str(escape(text))))


_env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(default=True))
_env.filters["emphasize"] = emphasize


def render(name: str | None, photos: list[str], books: list[dict], portrait: dict) -> str:
    """Renders the CV1 generated shape; kept as the converter's visual reference."""
    return _render(name, photos, portrait["lens"], books, build_shelves(books, portrait))


def render_file(
    shelf: ShelfFile,
    photos: list[str],
    cover_assets: Mapping[tuple[int, int], str] | None = None,
) -> str:
    """Renders only what the editable, versioned shelf and prepared assets say."""
    books, shelves = shelves_from_file(shelf.shelves, cover_assets)
    return _render(shelf.name, photos, shelf.lens, books, shelves)


def _render(name: str | None, photos: list[str], lens: str, books: list[dict], shelves: list[dict]) -> str:
    return _env.get_template("shelf.html").render(
        name=name,
        photos=list(zip(photos, mosaic(len(photos)), strict=True)),
        lens=lens,
        authors=frequent_authors(books),
        shelves=shelves,
        title_font="data:font/woff2;base64," + base64.b64encode(TITLE_FONT.read_bytes()).decode(),
    )
