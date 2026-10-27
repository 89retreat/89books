"""Turns the portrait themes into shelves of drawn spines, and lays out the photo mosaic."""

import hashlib
import re

from shelf.text import THRESHOLD, similarity

REST_TITLE = "E mais livros que já me acompanharam"
SIDE_MAX = 8  # shelves with this many books or fewer go to the side column on wide screens
PHONE_PHOTOS = 5
REST_FACE_EVERY = 9

# A few saturated accents among calm neutrals; the flag marks light spines, which take dark text.
PALETTE = [
    ("#1f2a44", False), ("#e4572e", False), ("#f2b134", True), ("#2f6f62", False),
    ("#e9e4da", True), ("#3a3a3c", False), ("#7aa6c2", True), ("#c9a7a0", True),
    ("#14213d", False), ("#d4d0c8", True), ("#8b9a6b", False), ("#b23a48", False),
]  # fmt: skip
LABEL_MAX = 46

_NUMERALS = [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def roman(number: int) -> str:
    result = ""
    for value, numeral in _NUMERALS:
        while number >= value:
            result += numeral
            number -= value
    return result


def _digest(title: str) -> int:
    """Stable number from the title, so a book looks the same every time the shelf is generated."""
    return int(hashlib.md5(title.encode()).hexdigest(), 16)


_SUFFIXES = {"jr", "jr.", "junior", "júnior", "filho", "neto", "sobrinho"}


def surname(author: str) -> str:
    """How a spine names the author: the last name, with a family suffix such as Junior kept."""
    parts = author.split()
    if len(parts) > 2 and parts[-1].lower() in _SUFFIXES:
        return " ".join(parts[-2:])
    return parts[-1] if parts else ""


def spine(title: str, authors: list[str] | None = None) -> dict:
    h = _digest(title)
    color, light = PALETTE[h % len(PALETTE)]
    label = title if len(title) <= LABEL_MAX else title[: LABEL_MAX - 2].rstrip() + "…"
    author = surname(authors[0]) if authors else ""
    return {
        "color": color,
        "light": light,
        "height": 192 + (h >> 8) % 48,
        # longer titles get thicker books, and the author's name needs a column of its own
        "width": max(30, min(62, 26 + len(title) // 2 + (8 if author else 0))),
        "label": label,
        "author": author,
    }


def tilt(title: str) -> tuple[float, int]:
    """Angle in degrees, either direction, and a small lift for a book shown face out."""
    h = _digest(title)
    angle = 1.2 + (h % 30) / 10
    return (-angle if (h >> 5) % 2 else angle), (h >> 9) % 6


def _cited(text: str) -> list[str]:
    return re.findall(r"\*([^*\n]+)\*", text)


def _has_cover(book: dict) -> bool:
    return bool(book.get("cover_id") or book.get("cover_url"))


def _book(book: dict, face: bool) -> dict:
    title = book.get("ol_title") or book["title"]
    angle, lift = tilt(title)
    return {
        **book,
        "title": title,
        "face": bool(face and _has_cover(book)),
        "spine": spine(title, book.get("authors")),
        "angle": angle,
        "lift": lift,
    }


def build_shelves(books: list[dict], portrait: dict) -> list[dict]:
    shelves, used = [], set()
    for theme in portrait.get("themes", []):
        indexes = [i for i in theme.get("books", []) if 0 <= i < len(books) and i not in used]
        if not indexes:
            continue
        used.update(indexes)
        cited = _cited(theme.get("text", ""))
        items = []
        for i in indexes:
            title = books[i].get("ol_title") or books[i]["title"]
            face = any(similarity(c, title) >= THRESHOLD for c in cited)
            items.append(_book(books[i], face))
        shelves.append(
            {"title": theme["title"], "text": theme.get("text", ""), "books": items, "rest": False}
        )

    rest = [b for i, b in enumerate(books) if i not in used]
    if rest:
        # the closing shelf is not a theme of the portrait: no paragraph and no numeral
        shelves.append(
            {
                "title": REST_TITLE,
                "text": "",
                "books": [_book(b, j % REST_FACE_EVERY == REST_FACE_EVERY // 2) for j, b in enumerate(rest)],
                "rest": True,
            }
        )

    for n, shelf in enumerate(shelves, start=1):
        shelf["numeral"] = "" if shelf["rest"] else roman(n)
        shelf["order"] = n
        small = n > 1 and len(shelf["books"]) <= SIDE_MAX  # the page always opens with the first shelf
        shelf["place"] = "full" if shelf["rest"] else ("side" if small else "wide")
    return shelves


def _row(count: int) -> list[int]:
    """Column spans that fill a row of four with `count` photos."""
    return {1: [4], 2: [2, 2], 3: [2, 1, 1], 4: [1, 1, 1, 1]}[count]


def mosaic(count: int) -> list[dict]:
    """Grid spans for a four-column mosaic: the cover photo is large, the others fill around it.

    On phones the grid has two columns and shows at most PHONE_PHOTOS photos; the last visible one
    says how many more there are, and all of them can be seen in the enlarged view.
    """
    if count == 0:
        return []
    if count == 1:
        spans = [(4, 2)]
    else:
        beside = min(count - 1, 4)
        spans = [(2, 2)] + {1: [(2, 2)], 2: [(2, 1), (2, 1)], 3: [(2, 1), (1, 1), (1, 1)], 4: [(1, 1)] * 4}[
            beside
        ]
        remaining = count - 1 - beside
        while remaining:
            chunk = min(remaining, 4)
            spans += [(c, 1) for c in _row(chunk)]
            remaining -= chunk
    visible = min(count, PHONE_PHOTOS)
    tiles = []
    for i, (cols, rows) in enumerate(spans):
        tiles.append(
            {
                "cols": cols,
                "rows": rows,
                "phone": i < visible,
                # with an odd number of small photos on phones, the last visible one takes the full row
                "phone_wide": i == visible - 1 and i > 0 and (visible - 1) % 2 == 1,
                "more": count - visible if i == visible - 1 else 0,
            }
        )
    return tiles
