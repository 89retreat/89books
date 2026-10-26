"""Normalization and comparison of book titles and authors."""

import re
import unicodedata
from difflib import SequenceMatcher

THRESHOLD = 0.82

_EDITION = re.compile(r"\b\d+\s*(?:a|o|st|nd|rd|th)?\s*(?:ed|edicao|edition|editio)\w*\b")
_EDITION_ORIGINAL = re.compile(
    r"[,\s]*\b\d+\s*(?:ª|º|a|o|st|nd|rd|th)?\s*(?:ed|edição|edicao|edition|editio)\w*\.?", re.IGNORECASE
)
_IGNORED_NAMES = {"et", "al", "org", "friends", "jr", "junior", "filho", "neto"}


def _strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def _normalize(text: str) -> str:
    text = _EDITION.sub(" ", text)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text).split())


def _prepare(title: str) -> str:
    text = _strip_accents(title or "").lower().replace("…", " ").replace("...", " ")
    return re.sub(r"\([^)]*\)", " ", text)


def normalize_title(title: str) -> str:
    text = _prepare(title)
    main = text.split(":", 1)[0]
    return _normalize(main if main.strip() else text)


def _variants(title: str) -> set[str]:
    """Title without subtitle, whole title and the part after the colon."""
    text = _prepare(title)
    parts = {normalize_title(title), _normalize(text)}
    if ":" in text:
        parts.add(_normalize(text.split(":", 1)[1]))
    return {p for p in parts if p}


def search_title(title: str) -> str:
    """Clean title for Open Library queries, keeping accents and case."""
    text = re.sub(r"\([^)]*\)", " ", title or "").replace("…", " ").replace("...", " ")
    main = text.split(":", 1)[0]
    text = _EDITION_ORIGINAL.sub(" ", main if main.strip() else text)
    return " ".join(text.split()).strip(" ,;-")


def _compare(a: str, b: str) -> float:
    if a == b:
        return 1.0
    short, long = sorted((a, b), key=len)
    if len(short) >= 8 and long.startswith(short + " "):
        return 0.95
    if len(short) >= 10 and long.endswith(" " + short):
        return 0.9
    ratio = SequenceMatcher(None, a, b).ratio()
    numbers_a, numbers_b = set(re.findall(r"\d+", a)), set(re.findall(r"\d+", b))
    if numbers_a and numbers_b and numbers_a != numbers_b:
        return min(ratio, 0.5)
    return ratio


def similarity(a: str, b: str) -> float:
    va, vb = _variants(a), _variants(b)
    if not va or not vb:
        return 0.0
    return max(_compare(x, y) for x in va for y in vb)


def surnames(authors) -> set[str]:
    result = set()
    for author in authors or []:
        parts = [p for p in re.split(r"[^a-z]+", _strip_accents(author).lower()) if p]
        parts = [p for p in parts if p not in _IGNORED_NAMES]
        if parts:
            result.add(parts[-1])
    return result
