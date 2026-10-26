"""Links each book to an Open Library work, with a local cache."""

import json
import time
from pathlib import Path

import httpx

from shelf.text import normalize_title, search_title, similarity, surnames

URL = "https://openlibrary.org/search.json"
FIELDS = "key,title,author_name,cover_i"
USER_AGENT = "89books/0.1 (+https://github.com/89retreat/89books)"
INTERVAL = 0.4  # Open Library asks for at most ~3 requests per second


class OpenLibrary:
    def __init__(self, cache_path: Path):
        self.cache_path = cache_path
        self.cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
        self.client = httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=30)
        self._last = 0.0

    def save(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(self.cache, ensure_ascii=False, indent=1), encoding="utf-8")

    def _search(self, params: dict) -> list[dict]:
        wait = INTERVAL - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        for attempt in range(3):
            try:
                response = self.client.get(URL, params={**params, "fields": FIELDS, "limit": 5})
                self._last = time.monotonic()
                if response.status_code == 200:
                    return response.json().get("docs", [])
            except httpx.HTTPError:
                pass
            time.sleep(2 * (attempt + 1))
        return []

    def lookup(self, title: str, authors: list[str]) -> dict | None:
        key = normalize_title(title) + "|" + ",".join(sorted(surnames(authors)))
        if key in self.cache:
            return self.cache[key]
        query = search_title(title)
        attempts = ([{"title": query, "author": authors[0]}] if authors else []) + [
            {"title": query},
            {"q": query},
        ]
        found = None
        for params in attempts:
            for doc in self._search(params):
                if similarity(title, doc.get("title", "")) >= 0.6:
                    found = {
                        "work": doc.get("key"),
                        "ol_title": doc.get("title"),
                        "cover_id": doc.get("cover_i"),
                    }
                    break
            if found:
                break
        self.cache[key] = found
        return found
