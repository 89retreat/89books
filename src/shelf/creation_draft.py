"""Private, resumable paid preparation saved before the final portrait call."""

from pathlib import Path

import yaml

from shelf.books import read_books_yaml
from shelf.core import CreationDraft

VERSION = 1


class DraftError(ValueError):
    """A saved creation draft is corrupt or incompatible with this version."""


def dump_draft(draft: CreationDraft) -> str:
    """Serializes only portable paid results: never keys, image bytes or absolute paths."""
    for book in draft.books:
        photo = book.get("photo") if isinstance(book, dict) else None
        if photo is not None and not _safe_photo_name(photo):
            raise DraftError("Could not save creation: book photo provenance must be a file name.")
    data = {
        "version": VERSION,
        "name": draft.name,
        "photos": list(draft.photos),
        "books": [dict(book) for book in draft.books],
        "left_out": [dict(book) for book in draft.left_out],
        "cost": draft.cost,
        "migrated": draft.migrated,
    }
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)


def parse_draft(text: str) -> CreationDraft:
    """Reads the private checkpoint strictly enough that recovery never guesses."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise DraftError(f"Could not read saved creation: {exc}") from exc
    if not isinstance(data, dict):
        raise DraftError("Could not read saved creation: the draft must be a mapping.")
    if data.get("version") != VERSION:
        raise DraftError(f"Could not read saved creation: unsupported version {data.get('version')!r}.")

    name = data.get("name")
    if name is not None and not isinstance(name, str):
        raise DraftError("Could not read saved creation: name must be text or null.")
    photos = data.get("photos")
    if not isinstance(photos, list) or not photos or any(not _safe_photo_name(photo) for photo in photos):
        raise DraftError("Could not read saved creation: photo names must be non-empty file names.")
    if len(set(photos)) != len(photos):
        raise DraftError("Could not read saved creation: photo names must not repeat.")

    try:
        books, left_out = read_books_yaml(
            yaml.safe_dump(
                {"books": data.get("books"), "left_out": data.get("left_out") or []},
                allow_unicode=True,
                sort_keys=False,
            )
        )
    except ValueError as exc:
        raise DraftError(f"Could not read saved creation books: {exc}") from exc

    cost = data.get("cost")
    if isinstance(cost, bool) or not isinstance(cost, int | float) or cost < 0:
        raise DraftError("Could not read saved creation: cost must be a non-negative number.")
    migrated = data.get("migrated")
    if not isinstance(migrated, bool):
        raise DraftError("Could not read saved creation: migrated must be true or false.")
    return CreationDraft(
        name=name,
        photos=list(photos),
        books=books,
        left_out=left_out,
        cost=round(float(cost), 4),
        migrated=migrated,
    )


def _safe_photo_name(value: object) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and value == Path(value).name
        and "\\" not in value
        and value not in {".", ".."}
    )
