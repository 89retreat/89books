"""The shelf, without the terminal: generating a shelf from photos and drawing its page.

The command line, and later a server, call these functions and decide what to ask, show and write.
Nothing here prints, reads input, looks at the environment or chooses a folder: progress and messages
go through the `log` and `progress` given by the caller, and the result comes back as data.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from shelf import photos as photo_tools
from shelf.books import dedupe
from shelf.page import render
from shelf.review import apply_review, confirm, name_books, settle
from shelf.text import normalize_title


@dataclass
class Shelf:
    """Everything the page is drawn from."""

    name: str | None
    photos: list[str]  # file names, the one that opens the page first
    books: list[dict]
    left_out: list[dict]
    portrait: dict
    cost: float = 0.0


@dataclass
class Services:
    """What generating a shelf calls outside: the model, the catalogues and the cover check."""

    recognize: Callable  # (jpeg, api_key) -> (books, cost)
    review: Callable  # (books, api_key) -> (entries, cost, names)
    portrait: Callable  # (books, api_key) -> (portrait, cost)
    library: object  # Open Library: lookup(title, authors), save()
    covers: object  # ok(cover), save()
    second: object | None = None  # Google Books, when there is a key


class Quiet:
    """Progress that shows nothing, for callers that do not show progress."""

    def start(self, total: int) -> None:
        pass

    def step(self, title: str) -> None:
        pass

    def finish(self) -> None:
        pass


@dataclass
class _Run:
    log: Callable[[str], None]
    progress: object
    cost: float = 0.0
    names: dict = field(default_factory=dict)


def generate(
    photos: list[Path],
    api_key: str,
    name: str | None,
    services: Services,
    log: Callable[[str], None] = lambda line: None,
    progress=None,
) -> Shelf:
    """Reads the photos, checks the books in the catalogues and writes the portrait. This is what costs."""
    run = _Run(log, progress or Quiet())
    books = _recognize(photos, api_key, services, run)
    _look_up(books, services.library, run)
    books, left_out = _review(books, api_key, services, run)
    books = _confirm(books, services.second, run)
    books = name_books(books, run.names)
    _covers(books, services, run)

    log("Writing your portrait...")
    portrait, spent = services.portrait(books, api_key)
    run.cost += spent
    return Shelf(name, [p.name for p in photos], books, left_out, portrait, round(run.cost, 4))


def draw(shelf: Shelf, images: list[str]) -> str:
    """The page, from the shelf and its photos as data URIs, in the shelf's photo order. Costs nothing."""
    return render(shelf.name, images, shelf.books, shelf.portrait)


def _recognize(photos: list[Path], api_key: str, services: Services, run: _Run) -> list[dict]:
    run.log(f"Recognizing books in {len(photos)} photos...")
    found: list[dict] = []
    for path in photos:
        books, spent = services.recognize(photo_tools.prepare(path), api_key)
        run.cost += spent
        found.extend({**book, "photo": path.name} for book in books)
        run.log(f"  {path.name}: {len(books)} books")
    books = dedupe(found)
    run.log(f"Recognized {len(books)} books.")
    return books


def _look_up(books: list[dict], library, run: _Run) -> None:
    run.log("Looking them up on Open Library...")
    run.progress.start(len(books))
    for book in books:
        run.progress.step(book["title"])
        book.update(library.lookup(book["title"], book.get("authors") or []) or {})
    run.progress.finish()
    library.save()


def _review(books: list[dict], api_key: str, services: Services, run: _Run) -> tuple[list[dict], list[dict]]:
    run.log("Checking titles and authors across the shelf...")
    # the review also says how each long-named author is known, for the spines
    entries, spent, run.names = services.review(books, api_key)
    run.cost += spent
    books, left_out = apply_review(books, entries)
    books = [settle(b) for b in books]
    corrected = sum(1 for b in books if b.get("source") == "review")
    run.log(f"  {corrected} corrected, {len(left_out)} left out.")
    return books, left_out


def _confirm(books: list[dict], second, run: _Run) -> list[dict]:
    if second is None:
        run.log("  Skipping Google Books: set GOOGLE_BOOKS_API_KEY to check titles in a second catalogue.")
        return books
    # books no catalogue has confirmed yet, with the reviewed title and author, which Google Books needs
    run.log("Confirming the rest on Google Books...")
    unconfirmed = [i for i, b in enumerate(books) if b.get("source") in ("review", "photo")]
    confirmed = 0
    run.progress.start(len(unconfirmed))
    for i in unconfirmed:
        run.progress.step(books[i]["title"])
        found = second.lookup(books[i]["title"], books[i].get("authors") or [])
        if found:
            books[i] = confirm(books[i], found)
            confirmed += 1
    run.progress.finish()
    second.save()
    run.log(f"  {confirmed} of {len(unconfirmed)} confirmed.")
    return books


def _covers(books: list[dict], services: Services, run: _Run) -> None:
    run.log("Fetching covers...")
    rejected = 0
    run.progress.start(len(books))
    for book in books:
        run.progress.step(book["title"])
        # a corrected title was searched under the misreading; search again under the right one
        if book.get("source") in ("review", "google_books") and normalize_title(
            book["title"]
        ) != normalize_title(book.get("read_as", "")):
            for key in ("work", "cover_id"):
                book.pop(key, None)
            match = services.library.lookup(book["title"], book.get("authors") or []) or {}
            book.update({k: v for k, v in match.items() if k in ("work", "cover_id")})
        if book.get("cover_id") and not services.covers.ok(book["cover_id"]):
            book.pop("cover_id")
            rejected += 1
        gb_cover = book.pop("gb_cover", None)
        if not book.get("cover_id") and gb_cover and services.covers.ok(gb_cover):
            book["cover_url"] = gb_cover
    run.progress.finish()
    services.library.save()
    services.covers.save()
    with_work = sum(1 for b in books if b.get("work"))
    with_cover = sum(1 for b in books if b.get("cover_id") or b.get("cover_url"))
    run.log(f"  {with_work} found, {with_cover} with covers ({rejected} scans of pages left out).")
