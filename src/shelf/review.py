"""Checks the recognized books as a whole shelf: titles, authors, duplicates and things that are not books.

Spines are read one photo at a time and catalogues match one title at a time, so a misread feminine ending
("Continuo Preto" for Sueli Carneiro's "Continuo Preta") or an author's name read as a title goes straight
to the page. Seen together, the shelf gives the model the context to fix them. It only answers for the books
it would change, which keeps the call cheap.
"""

import json
import re

from shelf import openrouter
from shelf.shelves import NAME_MAX, author_key
from shelf.text import normalize_title

PROMPT = """Você revisa a lista de livros de uma estante pessoal brasileira. Cada linha mostra o que foi lido na lombada por reconhecimento automático de fotos e, quando houver, o que a Open Library e o Google Books encontraram para aquela leitura. As leituras podem ter erros (letras trocadas, gênero ou número errado, título truncado, nome do autor lido como título), e os catálogos podem ter encontrado o livro errado.

Use o contexto da estante inteira e o seu conhecimento de livros para conferir cada item. Responda só sobre os itens que precisam mudar:
- title e authors: o título exato da edição mais provável nesta estante (em português, se for uma edição brasileira) e quem escreveu. Corrija só quando tiver segurança; na dúvida, não inclua o item.
- same_as: o número de outro item quando os dois forem o mesmo livro.
- not_a_book: true quando o item não for um livro (um objeto, uma editora, uma coleção sem título).

Depois, em known_as, diga como os autores de nome longo listados ao final são conhecidos pelos leitores, com no máximo 24 caracteres: o nome da capa dos livros, sempre com nome e sobrenome, nunca só o sobrenome. Exemplos: "Gabriel García Márquez", "João Ubaldo Ribeiro", "Ana Fani A. Carlos". Para uma instituição ou evento, um nome curto. A chave é o nome exatamente como listado.

Responda apenas com JSON:
{{"books": [{{"n": 3, "title": "...", "authors": ["..."]}}, {{"n": 7, "same_as": 2}}, {{"n": 9, "not_a_book": true}}],
 "known_as": {{"Gabriel José de la Concordia García Márquez": "Gabriel García Márquez"}}}}

Livros:
{books}

Autores de nome longo:
{long_names}"""


def _who(title: str | None, authors: list[str] | None) -> str:
    return f"{title} — {', '.join(authors)}" if authors else f"{title}"


def book_lines(books: list[dict]) -> str:
    lines = []
    for number, book in enumerate(books, start=1):
        parts = [f"{number}. lido: {_who(book['title'], book.get('authors'))}"]
        if book.get("ol_title"):
            parts.append(f"Open Library: {_who(book['ol_title'], book.get('ol_authors'))}")
        if book.get("gb_title"):
            parts.append(f"Google Books: {_who(book['gb_title'], book.get('gb_authors'))}")
        lines.append(" | ".join(parts))
    return "\n".join(lines)


def parse_review(text: str, book_count: int) -> dict[int, dict]:
    """Maps 0-based book indexes to the change the model asked for; invalid entries are dropped."""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        return {}
    try:
        items = json.loads(text[start : end + 1]).get("books") or []
    except json.JSONDecodeError:
        # a stray quote inside one title breaks the whole answer; keep every item that still reads
        items = []
        for chunk in re.findall(r"\{[^{}]*\}", text[start + 1 : end]):
            try:
                items.append(json.loads(chunk))
            except json.JSONDecodeError:
                continue
    entries: dict[int, dict] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        number = item.get("n")
        if not isinstance(number, int) or not 1 <= number <= book_count or number - 1 in entries:
            continue
        same_as = item.get("same_as")
        if isinstance(same_as, int) and 1 <= same_as <= book_count and same_as != number:
            entries[number - 1] = {"same_as": same_as - 1}
        elif item.get("not_a_book") is True:
            entries[number - 1] = {"not_a_book": True}
        elif isinstance(item.get("title"), str) and item["title"].strip():
            authors = [a.strip() for a in item.get("authors") or [] if isinstance(a, str) and a.strip()]
            entries[number - 1] = {"title": item["title"].strip(), "authors": authors}
    return entries


def long_names(books: list[dict]) -> list[str]:
    """First authors whose names do not fit a spine: the only ones the rule would have to shorten."""
    names: dict[str, str] = {}
    for book in books:
        first = " ".join(
            ((book.get("authors") or book.get("ol_authors") or book.get("gb_authors") or [""])[0]).split()
        )
        if len(first) > NAME_MAX:
            names.setdefault(author_key(first), first)
    return list(names.values())


def parse_names(text: str) -> dict[str, str]:
    """How each author is known, keyed by author_key so catalogue spellings of the same person match.

    Read pair by pair, so an answer cut short or broken by a stray quote in a title still yields the names.
    """
    start = text.find('"known_as"')
    if start == -1:
        return {}
    names = {}
    for author, name in re.findall(r'"([^"\n]+)"\s*:\s*"([^"\n]*)"', text[start:]):
        if name.strip() and author_key(author):
            names[author_key(author)] = " ".join(name.split())
    return names


def name_books(books: list[dict], names: dict[str, str]) -> list[dict]:
    """Records the name readers know for each book's first author, when the review gave one."""
    named = []
    for book in books:
        book = dict(book)
        first = (book.get("authors") or [""])[0]
        if known := names.get(author_key(first)):
            book["known_as"] = known
        named.append(book)
    return named


def apply_review(books: list[dict], entries: dict[int, dict]) -> tuple[list[dict], list[dict]]:
    """Returns the books kept, corrected where asked, and the ones left out, each with a reason."""
    books = [dict(b) for b in books]
    for i, entry in entries.items():
        if "title" in entry:
            book = books[i]
            if entry["title"] != book["title"]:
                book["read_as"] = book["title"]
            book["title"] = entry["title"]
            book["authors"] = entry["authors"] or book.get("authors") or []
            book["source"] = "review"
    removed: dict[int, str] = {}
    for i, entry in entries.items():
        if entry.get("not_a_book"):
            removed[i] = "not a book"
    for i, entry in entries.items():
        target = entry.get("same_as")
        if target is None or i in removed or target in removed:
            continue
        if not books[target].get("authors") and books[i].get("authors"):
            books[target]["authors"] = books[i]["authors"]
        removed[i] = f"same book as {books[target]['title']}"
    kept = [b for i, b in enumerate(books) if i not in removed]
    left_out = [{"title": books[i]["title"], "reason": removed[i]} for i in sorted(removed)]
    return kept, left_out


def settle(book: dict) -> dict:
    """Decides the title and authors shown: the review's, then Open Library's, then Google Books', then the photo's."""
    book = dict(book)
    ol_title, ol_authors = book.pop("ol_title", None), book.pop("ol_authors", None) or []
    gb_title, gb_authors = book.pop("gb_title", None), book.pop("gb_authors", None) or []
    if book.get("source") != "review":
        read = book["title"]
        if ol_title:
            book["title"], book["source"] = ol_title, "open_library"
        elif gb_title:
            book["title"], book["source"] = gb_title, "google_books"
        else:
            book["source"] = "photo"
        if book["title"] != read:
            book["read_as"] = read
    book["authors"] = book.get("authors") or ol_authors or gb_authors
    return book


def confirm(book: dict, found: dict) -> dict:
    """A title found in Google Books for this book and author replaces the spelling read from the spine."""
    book = dict(book)
    if normalize_title(found["gb_title"]) != normalize_title(book["title"]):
        book.setdefault("read_as", book["title"])
        book["title"] = found["gb_title"]
    book["source"] = "google_books"
    book["authors"] = book.get("authors") or found["gb_authors"]
    book["gb_cover"] = found.get("gb_cover")
    return book


def review_books(books: list[dict], api_key: str) -> tuple[dict[int, dict], float, dict[str, str]]:
    text, cost = openrouter.complete(
        api_key,
        PROMPT.format(books=book_lines(books), long_names="\n".join(long_names(books)) or "(nenhum)"),
        max_tokens=10000,
        temperature=0,
    )
    return parse_review(text, len(books)), cost, parse_names(text)
