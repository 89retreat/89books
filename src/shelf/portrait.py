"""Writes the reader portrait: the lens and the recurring themes of a shelf."""

import json

from shelf import openrouter

PROMPT = """Você recebe a lista de livros de uma estante pessoal, reconhecidos automaticamente a partir de fotos. Pode haver erros de leitura e itens que não são livros; ignore o que não fizer sentido.

Escreva um retrato curto, em português do Brasil, dirigido à própria pessoa ("você"), com duas partes:

- lente: uma frase sobre o modo de olhar o mundo que esta estante revela.
- temas: de três a cinco temas que se repetem, cada um com um nome curto e um parágrafo breve que cite dois ou três livros da lista. Marque cada título citado entre asteriscos, como *Torto Arado*.

Tom: observação atenta e generosa, de quem gosta de livros e de gente. Nada de elogio, julgamento, diagnóstico de personalidade ou frases genéricas que serviriam para qualquer leitor. Seja específico a esta estante. Não mencione que a lista veio de fotos nem os possíveis erros.

Responda apenas com JSON:
{{"lens": "...", "themes": [{{"name": "...", "text": "..."}}]}}

Livros:
{books}"""


def book_list(books: list[dict]) -> str:
    lines: list[str] = []
    for book in books:
        title = book.get("ol_title") or book["title"]
        authors = ", ".join(book.get("authors") or [])
        line = f"- {title} — {authors}" if authors else f"- {title}"
        if line not in lines:
            lines.append(line)
    return "\n".join(lines)


def parse_portrait(text: str) -> dict:
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("portrait response has no JSON")
    data = json.loads(text[start : end + 1])
    lens = data.get("lens")
    if not isinstance(lens, str) or not lens.strip():
        raise ValueError("portrait response has no lens")
    themes = [
        {"name": str(t.get("name", "")).strip(), "text": str(t.get("text", "")).strip()}
        for t in data.get("themes") or []
        if isinstance(t, dict)
    ]
    return {"lens": lens.strip(), "themes": themes}


def write_portrait(books: list[dict], api_key: str) -> tuple[dict, float]:
    text, cost = openrouter.complete(
        api_key, PROMPT.format(books=book_list(books)), max_tokens=2000, temperature=0.7
    )
    return parse_portrait(text), cost
