"""The shelf, without the terminal: generating a shelf from photos and drawing its page.

The command line, and later a server, call these functions and decide what to ask, show and write.
Nothing here prints, reads input, looks at the environment or chooses a folder: progress and messages
go through the `log` and `progress` given by the caller, and the result comes back as data.
"""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path

from shelf import photos as photo_tools
from shelf.books import dedupe, read_books_yaml
from shelf.page import render_file
from shelf.review import apply_review, confirm, name_books, settle
from shelf.shelf_file import LeftOutBook, ShelfBook, ShelfFile, ShelfSection
from shelf.shelves import build_shelves
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
class Creation:
    """The source file produced by a paid creation, before a client decides where to save it."""

    shelf: ShelfFile
    books: int
    cost: float
    migrated: bool


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


def create(
    photos: list[Path],
    api_key: str,
    name: str | None,
    services: Services,
    legacy_books: str | None = None,
    log: Callable[[str], None] = lambda line: None,
    progress=None,
) -> Creation:
    """Creates the editable source once, either from photos or from the saved CV1 book list."""
    if legacy_books is None:
        generated = generate(photos, api_key, name, services, log, progress)
        migrated = False
    else:
        books, left_out = read_books_yaml(legacy_books)
        log(f"Reusing {len(books)} books from books.yaml; photos will not be read again.")
        log("Writing your portrait...")
        portrait, cost = services.portrait(books, api_key)
        generated = Shelf(
            name=name,
            photos=[photo.name for photo in photos],
            books=books,
            left_out=left_out,
            portrait=portrait,
            cost=round(cost, 4),
        )
        migrated = True
    source = _shelf_file(generated)
    return Creation(source, len(generated.books), generated.cost, migrated)


def draw(
    shelf: ShelfFile,
    images: list[str],
    cover_assets: Mapping[tuple[int, int], str] | None = None,
) -> str:
    """Draws the page from the editable source and prepared assets. Costs nothing."""
    return render_file(shelf, images, cover_assets)


def correct_book_identity(
    shelf: ShelfFile,
    shelf_index: int,
    book_index: int,
    *,
    title: str,
    authors: list[str],
    known_as: str | None,
) -> ShelfFile:
    """Returns a shelf copy with the reader's title, authors and spine name for one book."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must not be empty")
    if not isinstance(authors, list) or any(
        not isinstance(author, str) or not author.strip() for author in authors
    ):
        raise ValueError("authors must be a list of non-empty names")
    if known_as is not None and (not isinstance(known_as, str) or not known_as.strip()):
        raise ValueError("known_as must be non-empty text or None")
    return _replace_book(
        shelf,
        shelf_index,
        book_index,
        lambda book: replace(book, title=title, authors=list(authors), known_as=known_as),
    )


def set_book_cover(
    shelf: ShelfFile,
    shelf_index: int,
    book_index: int,
    cover: str | None,
) -> ShelfFile:
    """Returns a shelf copy with the reader's local, HTTPS, absent or `none` cover choice."""
    if cover is not None and (not isinstance(cover, str) or not cover.strip()):
        raise ValueError("cover must be non-empty text or None")
    return _replace_book(shelf, shelf_index, book_index, lambda book: replace(book, cover=cover))


def set_book_face(
    shelf: ShelfFile,
    shelf_index: int,
    book_index: int,
    face: bool | None,
) -> ShelfFile:
    """Returns a shelf copy with an explicit face/spine choice, or automatic when None."""
    if face is not None and not isinstance(face, bool):
        raise ValueError("face must be true, false or None")
    return _replace_book(shelf, shelf_index, book_index, lambda book: replace(book, face=face))


def move_book(
    shelf: ShelfFile,
    from_shelf_index: int,
    book_index: int,
    to_shelf_index: int,
    position: int | None = None,
) -> ShelfFile:
    """Moves one complete book to an authored position without mutating the source."""
    if from_shelf_index < 0 or book_index < 0 or to_shelf_index < 0:
        raise IndexError("shelf and book positions must not be negative")
    source = shelf.shelves[from_shelf_index]
    target = shelf.shelves[to_shelf_index]
    source_books = list(source.books)
    book = source_books.pop(book_index)
    sections = list(shelf.shelves)
    if from_shelf_index == to_shelf_index:
        source_books.insert(_insertion_position(position, len(source_books)), book)
        sections[from_shelf_index] = replace(source, books=source_books)
    else:
        target_books = list(target.books)
        target_books.insert(_insertion_position(position, len(target_books)), book)
        sections[from_shelf_index] = replace(source, books=source_books)
        sections[to_shelf_index] = replace(target, books=target_books)
    return replace(shelf, shelves=sections)


def add_shelf_section(
    shelf: ShelfFile,
    title: str,
    *,
    text: str = "",
    position: int | None = None,
) -> ShelfFile:
    """Adds an empty authored shelf section at one position or at the end."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("shelf title must not be empty")
    if not isinstance(text, str):
        raise ValueError("shelf text must be text")
    sections = list(shelf.shelves)
    sections.insert(_insertion_position(position, len(sections)), ShelfSection(title=title, text=text))
    return replace(shelf, shelves=sections)


def move_shelf_section(
    shelf: ShelfFile,
    shelf_index: int,
    position: int | None = None,
) -> ShelfFile:
    """Moves one complete shelf section to an authored position."""
    if shelf_index < 0:
        raise IndexError("shelf position must not be negative")
    sections = list(shelf.shelves)
    section = sections.pop(shelf_index)
    sections.insert(_insertion_position(position, len(sections)), section)
    return replace(shelf, shelves=sections)


def remove_shelf_section(shelf: ShelfFile, shelf_index: int) -> ShelfFile:
    """Removes an empty section; books must be moved explicitly before their shelf is removed."""
    if shelf_index < 0:
        raise IndexError("shelf position must not be negative")
    sections = list(shelf.shelves)
    section = sections[shelf_index]
    if section.books:
        raise ValueError(f'Shelf "{section.title}" is not empty; move its books before removing it')
    sections.pop(shelf_index)
    return replace(shelf, shelves=sections)


def _insertion_position(position: int | None, length: int) -> int:
    if position is None:
        return length
    if not isinstance(position, int) or position < 0 or position > length:
        raise IndexError(f"insertion position must be between 0 and {length}")
    return position


def hide_book(shelf: ShelfFile, shelf_index: int, book_index: int) -> ShelfFile:
    """Returns a shelf copy with one selected book hidden, for any client UI."""
    return _set_book_hidden(shelf, shelf_index, book_index, True)


def show_book(shelf: ShelfFile, shelf_index: int, book_index: int) -> ShelfFile:
    """Returns a shelf copy with the hidden mark removed from one selected book."""
    return _set_book_hidden(shelf, shelf_index, book_index, None)


def _set_book_hidden(shelf: ShelfFile, shelf_index: int, book_index: int, hidden: bool | None) -> ShelfFile:
    return _replace_book(
        shelf,
        shelf_index,
        book_index,
        lambda book: replace(book, hidden=hidden),
    )


def _replace_book(
    shelf: ShelfFile,
    shelf_index: int,
    book_index: int,
    change: Callable[[ShelfBook], ShelfBook],
) -> ShelfFile:
    if shelf_index < 0 or book_index < 0:
        raise IndexError("shelf and book positions must not be negative")
    section = shelf.shelves[shelf_index]
    books = list(section.books)
    books[book_index] = change(books[book_index])
    sections = list(shelf.shelves)
    sections[shelf_index] = replace(section, books=books)
    return replace(shelf, shelves=sections)


def _shelf_file(generated: Shelf) -> ShelfFile:
    if not generated.photos:
        raise ValueError("A shelf needs at least one photo.")
    sections = []
    for arranged in build_shelves(generated.books, generated.portrait):
        sections.append(
            ShelfSection(
                title=arranged["title"],
                text=arranged["text"],
                books=[_shelf_book(book) for book in arranged["books"]],
            )
        )
    left_out = [
        LeftOutBook(str(book["title"]), str(book["reason"]))
        for book in generated.left_out
        if isinstance(book, dict) and book.get("title") and book.get("reason")
    ]
    return ShelfFile(
        name=generated.name,
        cover_photo=generated.photos[0],
        lens=generated.portrait["lens"],
        shelves=sections,
        left_out=left_out,
    )


def _shelf_book(book: dict) -> ShelfBook:
    cover = book.get("cover_url")
    if not cover and book.get("cover_id"):
        cover = f"https://covers.openlibrary.org/b/id/{book['cover_id']}-M.jpg?default=false"
    return ShelfBook(
        title=book["title"],
        authors=list(book.get("authors") or []),
        known_as=book.get("known_as"),
        cover=cover,
        read_as=book.get("read_as"),
        source=book.get("source"),
        photo=book.get("photo"),
        work=book.get("work"),
    )


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
