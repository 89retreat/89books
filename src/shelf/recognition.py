"""Recognizes books in a shelf photo with a vision model."""

import json

from shelf import openrouter
from shelf.photos import data_uri

PROMPT = """Você recebe uma foto de livros: uma estante, uma prateleira ou uma tela da biblioteca do Kindle.
Liste todos os livros cujo título você consegue ler na imagem.

Regras:
- Inclua apenas livros cujo título esteja legível, ao menos em parte. Não adivinhe livros ilegíveis.
- Se o título estiver truncado ou cortado na borda, devolva o título completo só se reconhecer o livro com segurança; senão, devolva o trecho que lê.
- Autores: os que aparecem na imagem ou que você reconhece com segurança pelo título. Se não souber, lista vazia.
- Leia as lombadas, inclusive as verticais, e os livros deitados com título legível.
- Cada livro aparece uma vez por imagem.

Responda apenas com JSON, sem comentários:
{"books": [{"title": "...", "authors": ["..."]}]}"""


def parse_books(text: str) -> list[dict]:
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        return []
    data = json.loads(text[start : end + 1])
    books = data.get("books", []) if isinstance(data, dict) else data
    return [
        {"title": b["title"].strip(), "authors": [a for a in b.get("authors") or [] if isinstance(a, str)]}
        for b in books
        if isinstance(b, dict) and isinstance(b.get("title"), str) and b["title"].strip()
    ]


def recognize(jpeg: bytes, api_key: str) -> tuple[list[dict], float]:
    content = [
        {"type": "text", "text": PROMPT},
        {"type": "image_url", "image_url": {"url": data_uri(jpeg)}},
    ]
    text, cost = openrouter.complete(api_key, content, max_tokens=8000, temperature=0)
    return parse_books(text), cost
