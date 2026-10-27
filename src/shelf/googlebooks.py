"""Google Books as a second catalogue, for books Open Library did not find or found without authors.

It knows more Brazilian editions than Open Library. It needs a free Books API key: the anonymous quota
answers 429 from the first request. Searches are free text with the author, because the `intitle:`
operator returns nothing even for well-known titles (checked on 2026-10-27), and a misspelled title alone
finds unrelated books while the same title with its author finds the right one.
"""

import json
import time
from collections.abc import Callable
from difflib import SequenceMatcher
from pathlib import Path

import httpx

from shelf.text import THRESHOLD, normalize_title, search_title, similarity, surnames

URL = "https://www.googleapis.com/books/v1/volumes"
SPELLING = (
    0.9  # without an author: "Pobreza e Urbana" finds "Pobreza urbana", "Continuum Preta" not "Continuum"
)


def _fetch(params: dict) -> dict:
    for attempt in range(3):  # the API answers 503 now and then
        response = httpx.get(URL, params=params, timeout=30)
        if response.status_code != 503:
            break
        time.sleep(1 + attempt)
    response.raise_for_status()
    return response.json()


def _cover(info: dict) -> str | None:
    url = (info.get("imageLinks") or {}).get("thumbnail")
    if not url:
        return None
    return url.replace("http://", "https://", 1).replace("&edge=curl", "")


class GoogleBooks:
    def __init__(self, cache_path: Path, api_key: str, fetch: Callable[[dict], dict] = _fetch):
        self.cache_path = cache_path
        self.api_key = api_key
        self.fetch = fetch
        self.cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}

    def save(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(self.cache, ensure_ascii=False, indent=1), encoding="utf-8")

    @staticmethod
    def _same_book(title: str, authors: list[str], info: dict) -> bool:
        """With an author, the author must match and the title may differ by a subtitle. Without one,
        only a near-identical spelling counts: a shorter or neighbouring title is usually another book."""
        if authors:
            same_author = bool(surnames(authors) & surnames(info.get("authors") or []))
            return same_author and similarity(title, info.get("title", "")) >= THRESHOLD
        spelling = SequenceMatcher(None, normalize_title(title), normalize_title(info.get("title", "")))
        return spelling.ratio() >= SPELLING

    def lookup(self, title: str, authors: list[str]) -> dict | None:
        key = normalize_title(title) + "|" + ",".join(sorted(surnames(authors)))
        if key in self.cache:
            return self.cache[key]
        query = " ".join([search_title(title), *authors[:1]])
        try:
            items = self.fetch({"q": query, "maxResults": 5, "printType": "books", "key": self.api_key})
        except (OSError, httpx.HTTPError, ValueError):
            return None  # not cached: the next run tries again
        found = None
        for item in items.get("items") or []:
            info = item.get("volumeInfo") or {}
            if self._same_book(title, authors, info):
                found = {
                    "gb_title": info["title"],
                    "gb_authors": info.get("authors") or [],
                    "gb_cover": _cover(info),
                }
                break
        self.cache[key] = found
        return found
