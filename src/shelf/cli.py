"""Command line: `shelf <folder>` writes shelf.html and books.yaml into the folder."""

import argparse
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from shelf import photos as photo_tools
from shelf.books import dedupe, write_books_yaml
from shelf.config import Config, ConfigError, load_config
from shelf.openlibrary import OpenLibrary
from shelf.page import render
from shelf.portrait import write_portrait
from shelf.recognition import recognize

CACHE_DIR = ".shelf"


@dataclass
class Result:
    html: Path
    books_yaml: Path
    books: int
    cost: float


def build_shelf(
    config: Config,
    recognize: Callable = recognize,
    library=None,
    portrait: Callable = write_portrait,
    log: Callable[[str], None] = print,
) -> Result:
    library = library or OpenLibrary(config.folder / CACHE_DIR / "openlibrary.json")
    cost = 0.0
    images: list[str] = []
    found: list[dict] = []

    log(f"Recognizing books in {len(config.photos)} photos...")
    for path in config.photos:
        jpeg = photo_tools.prepare(path)
        images.append(photo_tools.data_uri(jpeg))
        books, spent = recognize(jpeg, config.api_key)
        cost += spent
        found.extend({**book, "photo": path.name} for book in books)
        log(f"  {path.name}: {len(books)} books")

    books = dedupe(found)
    log(f"Recognized {len(books)} books.")

    log("Looking them up on Open Library...")
    for book in books:
        book.update(library.lookup(book["title"], book.get("authors") or []) or {})
    library.save()
    with_work = sum(1 for b in books if b.get("work"))
    with_cover = sum(1 for b in books if b.get("cover_id"))
    log(f"  {with_work} found, {with_cover} with covers.")

    log("Writing your portrait...")
    reader_portrait, spent = portrait(books, config.api_key)
    cost += spent

    html_path = config.folder / "shelf.html"
    html_path.write_text(render(config.name, images, books, reader_portrait), encoding="utf-8")
    yaml_path = config.folder / "books.yaml"
    write_books_yaml(yaml_path, books)
    log(f"Done: {html_path.name} and {yaml_path.name} in {config.folder} (cost: US$ {cost:.2f})")
    return Result(html=html_path, books_yaml=yaml_path, books=len(books), cost=round(cost, 4))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="shelf",
        description="Generate a self-contained HTML bookshelf, with a reader portrait, from a folder of shelf photos.",
    )
    parser.add_argument("folder", type=Path, help="folder with photos of your shelf or shelves")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.folder)
    except ConfigError as exc:
        print(f"shelf: {exc}", file=sys.stderr)
        return 2
    build_shelf(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
