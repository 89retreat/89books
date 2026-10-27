"""Command line: `shelf <folder>` writes shelf.html and books.yaml into the folder."""

import argparse
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from shelf import photos as photo_tools
from shelf.books import dedupe, write_books_yaml
from shelf.config import Config, ConfigError, load_config
from shelf.covers import CoverCheck
from shelf.googlebooks import GoogleBooks
from shelf.openlibrary import OpenLibrary
from shelf.page import render
from shelf.portrait import write_portrait
from shelf.recognition import recognize
from shelf.review import apply_review, confirm, review_books, settle
from shelf.text import normalize_title

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
    covers=None,
    second=None,
    review: Callable = review_books,
    log: Callable[[str], None] = print,
) -> Result:
    cache = config.folder / CACHE_DIR
    library = library or OpenLibrary(cache / "openlibrary.json")
    covers = covers or CoverCheck(cache / "covers.json")
    if second is None and config.google_books_api_key:
        second = GoogleBooks(cache / "googlebooks.json", config.google_books_api_key)
    cost = 0.0
    images: list[str] = []
    found: list[dict] = []

    log(f"Recognizing books in {len(config.photos)} photos...")
    for path in config.photos:
        jpeg = photo_tools.prepare(path)
        images.append(photo_tools.data_uri(photo_tools.prepare(path, photo_tools.PAGE_SIDE)))
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

    log("Checking titles and authors across the shelf...")
    entries, spent = review(books, config.api_key)
    cost += spent
    books, left_out = apply_review(books, entries)
    books = [settle(b) for b in books]
    corrected = sum(1 for b in books if b.get("source") == "review")
    log(f"  {corrected} corrected, {len(left_out)} left out.")

    if second is None:
        log("  Skipping Google Books: set GOOGLE_BOOKS_API_KEY to check titles in a second catalogue.")
    else:
        # books no catalogue has confirmed yet, with the reviewed title and author, which Google Books needs
        log("Confirming the rest on Google Books...")
        unconfirmed = [i for i, b in enumerate(books) if b.get("source") in ("review", "photo")]
        confirmed = 0
        for i in unconfirmed:
            found = second.lookup(books[i]["title"], books[i].get("authors") or [])
            if found:
                books[i] = confirm(books[i], found)
                confirmed += 1
        second.save()
        log(f"  {confirmed} of {len(unconfirmed)} confirmed.")
    for book in books:
        # a corrected title was searched under the misreading; search again under the right one
        if book.get("source") in ("review", "google_books") and normalize_title(
            book["title"]
        ) != normalize_title(book.get("read_as", "")):
            for key in ("work", "cover_id"):
                book.pop(key, None)
            match = library.lookup(book["title"], book.get("authors") or []) or {}
            book.update({k: v for k, v in match.items() if k in ("work", "cover_id")})
    library.save()

    rejected = 0
    for book in books:
        if book.get("cover_id") and not covers.ok(book["cover_id"]):
            book.pop("cover_id")
            rejected += 1
        gb_cover = book.pop("gb_cover", None)
        if not book.get("cover_id") and gb_cover and covers.ok(gb_cover):
            book["cover_url"] = gb_cover
    covers.save()
    with_work = sum(1 for b in books if b.get("work"))
    with_cover = sum(1 for b in books if b.get("cover_id") or b.get("cover_url"))
    log(f"  {with_work} found, {with_cover} with covers ({rejected} scans of pages left out).")

    log("Writing your portrait...")
    reader_portrait, spent = portrait(books, config.api_key)
    cost += spent

    html_path = config.folder / "shelf.html"
    html_path.write_text(render(config.name, images, books, reader_portrait), encoding="utf-8")
    yaml_path = config.folder / "books.yaml"
    write_books_yaml(yaml_path, books, left_out)
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
