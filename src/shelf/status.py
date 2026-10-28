"""Derives the shelf's product state from facts supplied by a client.

There is no filesystem, clock, environment, terminal or network here. A CLI or server gathers facts and
uses the same state machine to decide what is safe to do next.
"""

from dataclasses import dataclass

from shelf.shelf_file import ShelfYamlError, ShelfYamlIssue, parse_shelf


@dataclass(frozen=True)
class ShelfFacts:
    photo_count: int = 0
    versions: int = 0
    source_text: str | None = None
    source_modified: float | None = None
    page_modified: float | None = None
    source_hash: str | None = None
    last_drawn_hash: str | None = None


@dataclass(frozen=True)
class ShelfStatus:
    state: str
    photo_count: int
    versions: int
    source_modified: float | None
    page_modified: float | None
    books: int | None = None
    visible_books: int | None = None
    hidden_books: int | None = None
    shelves: int | None = None
    errors: tuple[ShelfYamlIssue, ...] = ()
    next_command: str = "create"


def inspect(facts: ShelfFacts) -> ShelfStatus:
    """Returns one state and next safe verb from the current source and generated page facts."""
    if facts.source_text is None:
        return _result(facts, "not_created", next_command="create")
    try:
        shelf = parse_shelf(facts.source_text)
    except ShelfYamlError as error:
        return _result(facts, "invalid", errors=error.issues, next_command="check")

    books = sum(len(section.books) for section in shelf.shelves)
    hidden = sum(book.hidden is True for section in shelf.shelves for book in section.books)
    details = {
        "books": books,
        "visible_books": books - hidden,
        "hidden_books": hidden,
        "shelves": len(shelf.shelves),
    }
    if facts.page_modified is None:
        return _result(facts, "not_drawn", next_command="draw", **details)
    if facts.last_drawn_hash is not None:
        if facts.source_hash != facts.last_drawn_hash:
            return _result(facts, "stale", next_command="draw", **details)
    elif facts.source_modified is not None and facts.source_modified > facts.page_modified:
        return _result(facts, "stale", next_command="draw", **details)
    return _result(facts, "ready", next_command="open", **details)


def _result(facts: ShelfFacts, state: str, **values) -> ShelfStatus:
    return ShelfStatus(
        state=state,
        photo_count=facts.photo_count,
        versions=facts.versions,
        source_modified=facts.source_modified,
        page_modified=facts.page_modified,
        **values,
    )
