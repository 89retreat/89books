"""Renders the shelf page: photo mosaic, lens and the portrait themes as shelves."""

import base64
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

from shelf.shelves import build_shelves, mosaic

TEMPLATES = Path(__file__).parent / "templates"
TITLE_FONT = Path(__file__).parent / "fonts" / "newsreader-italic-500-latin.woff2"


def emphasize(text: str) -> Markup:
    """Escapes text, then turns *Book Title* into <em>Book Title</em>."""
    return Markup(re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", str(escape(text))))


_env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(default=True))
_env.filters["emphasize"] = emphasize


def render(name: str | None, photos: list[str], books: list[dict], portrait: dict) -> str:
    return _env.get_template("shelf.html").render(
        name=name,
        photos=list(zip(photos, mosaic(len(photos)), strict=True)),
        lens=portrait["lens"],
        shelves=build_shelves(books, portrait),
        title_font="data:font/woff2;base64," + base64.b64encode(TITLE_FONT.read_bytes()).decode(),
    )
