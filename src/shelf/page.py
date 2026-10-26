"""Renders the self-contained shelf page."""

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

TEMPLATES = Path(__file__).parent / "templates"


def emphasize(text: str) -> Markup:
    """Escapes text, then turns *Book Title* into <em>Book Title</em>."""
    return Markup(re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", str(escape(text))))


_env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(default=True))
_env.filters["emphasize"] = emphasize


def render(name: str | None, photos: list[str], books: list[dict], portrait: dict) -> str:
    title = f"A estante de {name}" if name else "Minha estante"
    return _env.get_template("shelf.html").render(title=title, photos=photos, books=books, portrait=portrait)
