"""Turns intentional photo file names into reader-authored shelf sections."""

import re
from dataclasses import dataclass
from pathlib import Path

_NAMED_PHOTO = re.compile(r"^(\d{2})_(.*)$")


class NamedShelfError(ValueError):
    """Intentional photo names conflict or cannot become safe shelf titles."""


@dataclass(frozen=True)
class NamedShelf:
    position: int
    title: str
    photo: str
    book_indexes: tuple[int, ...] = ()


def parse_named_photo(file_name: str) -> tuple[int, str] | None:
    """Returns an explicit shelf position and title, or None for ordinary photo names."""
    match = _NAMED_PHOTO.fullmatch(Path(file_name).stem)
    if match is None:
        return None
    position = int(match.group(1))
    title = " ".join(match.group(2).replace("_", " ").split())
    if not title:
        raise NamedShelfError(f'{file_name}: named shelf photos need a non-empty title after "NN_".')
    return position, title


def named_shelves(photo_names: list[str], books: list[dict]) -> list[NamedShelf]:
    """Builds ordered shelf hints from intentional names and per-book photo provenance."""
    shelves: list[NamedShelf] = []
    positions: dict[int, str] = {}
    titles: dict[str, str] = {}
    for photo in photo_names:
        parsed = parse_named_photo(photo)
        if parsed is None:
            continue
        position, title = parsed
        if previous := positions.get(position):
            raise NamedShelfError(
                f'Named shelf position {position:02d} is used by both "{previous}" and "{photo}".'
            )
        title_key = title.casefold()
        if previous := titles.get(title_key):
            raise NamedShelfError(
                f'Named shelf title "{title}" is repeated by both "{previous}" and "{photo}".'
            )
        positions[position] = photo
        titles[title_key] = photo
        indexes = tuple(index for index, book in enumerate(books) if book.get("photo") == photo)
        shelves.append(NamedShelf(position, title, photo, indexes))
    return sorted(shelves, key=lambda shelf: shelf.position)


def apply_named_shelves(portrait: dict, shelves: list[NamedShelf]) -> dict:
    """Keeps model prose while replacing arrangement with the reader's named photo shelves."""
    if not shelves:
        return portrait
    model_themes = portrait.get("themes") or []
    themes = []
    for index, shelf in enumerate(shelves):
        model_theme = model_themes[index] if index < len(model_themes) else {}
        themes.append(
            {
                "title": shelf.title,
                "text": str(model_theme.get("text") or "").strip(),
                "books": list(shelf.book_indexes),
                "photo": shelf.photo,
            }
        )
    return {"lens": portrait.get("lens", ""), "themes": themes}
