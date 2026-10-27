"""Command line: `shelf <folder>` writes shelf.html and books.yaml into the folder."""

import argparse
import os
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from shelf import photos as photo_tools
from shelf import setup
from shelf.books import dedupe, write_books_yaml
from shelf.config import PHOTO_EXTENSIONS, Config, ConfigError, load_config
from shelf.covers import CoverCheck
from shelf.googlebooks import GoogleBooks
from shelf.openlibrary import OpenLibrary
from shelf.page import render
from shelf.portrait import write_portrait
from shelf.progress import Progress
from shelf.recognition import recognize
from shelf.review import apply_review, confirm, name_books, review_books, settle
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
    progress=None,
) -> Result:
    progress = progress or Progress()
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
    progress.start(len(books))
    for book in books:
        progress.step(book["title"])
        book.update(library.lookup(book["title"], book.get("authors") or []) or {})
    progress.finish()
    library.save()

    log("Checking titles and authors across the shelf...")
    # the review also says how each author is known; a review that does not still answers (entries, cost)
    entries, spent, *rest = review(books, config.api_key)
    names = rest[0] if rest else {}
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
        progress.start(len(unconfirmed))
        for i in unconfirmed:
            progress.step(books[i]["title"])
            found = second.lookup(books[i]["title"], books[i].get("authors") or [])
            if found:
                books[i] = confirm(books[i], found)
                confirmed += 1
        progress.finish()
        second.save()
        log(f"  {confirmed} of {len(unconfirmed)} confirmed.")
    books = name_books(books, names)
    log("Fetching covers...")
    rejected = 0
    progress.start(len(books))
    for book in books:
        progress.step(book["title"])
        # a corrected title was searched under the misreading; search again under the right one
        if book.get("source") in ("review", "google_books") and normalize_title(
            book["title"]
        ) != normalize_title(book.get("read_as", "")):
            for key in ("work", "cover_id"):
                book.pop(key, None)
            match = library.lookup(book["title"], book.get("authors") or []) or {}
            book.update({k: v for k, v in match.items() if k in ("work", "cover_id")})
        if book.get("cover_id") and not covers.ok(book["cover_id"]):
            book.pop("cover_id")
            rejected += 1
        gb_cover = book.pop("gb_cover", None)
        if not book.get("cover_id") and gb_cover and covers.ok(gb_cover):
            book["cover_url"] = gb_cover
    progress.finish()
    library.save()
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


DEFAULT_FOLDER = Path("my-bookshelf")


def main(
    argv: list[str] | None = None,
    terminal: setup.Terminal | None = None,
    interactive: bool | None = None,
    build: Callable = build_shelf,
    check_openrouter: Callable = setup.check_openrouter,
    check_google: Callable = setup.check_google,
) -> int:
    parser = argparse.ArgumentParser(
        prog="shelf",
        description="Turn photos of your bookshelf into a shareable HTML page with a reader portrait.",
    )
    parser.add_argument(
        "folder",
        type=Path,
        nargs="?",
        default=DEFAULT_FOLDER,
        help="folder with your shelf photos (default: my-bookshelf)",
    )
    parser.add_argument("--setup", action="store_true", help="ask for your name and keys again")
    parser.add_argument("--yes", action="store_true", help="do not ask before spending")
    args = parser.parse_args(argv)
    terminal = terminal or setup.Terminal()
    interactive = setup.is_interactive() if interactive is None else interactive

    # photos come first: asking for keys only to find an empty folder would waste the person's time
    if args.folder.is_dir() and not any(
        p.suffix.lower() in PHOTO_EXTENSIONS for p in args.folder.iterdir() if p.is_file()
    ):
        print(
            f"shelf: No photos in {args.folder}. Put photos of your shelf in it (.jpg, .heic, .png or .webp) "
            "and run `uv run shelf` again.",
            file=sys.stderr,
        )
        return 2
    if interactive and args.folder.is_dir() and (args.setup or setup.needs_setup(args.folder, os.environ)):
        setup.run_setup(
            args.folder,
            os.environ,
            terminal,
            check_openrouter=check_openrouter,
            check_google=check_google,
            again=args.setup,
        )
    try:
        config = load_config(args.folder)
    except ConfigError as exc:
        print(f"shelf: {exc}", file=sys.stderr)
        return 2
    if interactive and not args.yes and not setup.confirm_cost(len(config.photos), terminal):
        terminal.say("Nothing was spent.")
        return 0
    build(config)
    page = config.folder / "shelf.html"
    opener = "open" if sys.platform == "darwin" else "start" if os.name == "nt" else "xdg-open"
    terminal.say()
    terminal.say(f"Your shelf is ready: {page}")
    terminal.say(f"Open it in your browser with `{opener} {page}`.")
    terminal.say("To share it, send the file itself (WhatsApp, AirDrop, email) and open it in a browser.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
