"""Writes the reader portrait: the lens and the themes that become the shelves of the page."""

import json

from shelf import openrouter

PROMPT = """Você recebe a lista numerada dos livros de uma estante pessoal, reconhecidos automaticamente a partir de fotos. Pode haver erros de leitura e itens que não são livros; ignore o que não fizer sentido.

Escreva o retrato desta estante em português do Brasil, em primeira pessoa, como se a dona ou o dono estivesse apresentando os próprios livros a uma visita ("eu olho o mundo...", "boa parte da minha estante..."). Tom de conversa acolhedora: a pessoa mostra o que ama, sem se elogiar. Nada de diagnóstico de personalidade nem de frases genéricas que serviriam para qualquer leitor. Não mencione que a lista veio de fotos nem os possíveis erros.

- lens: uma frase sobre o modo de olhar o mundo que esta estante revela.
- themes: de três a seis temas que se repetem. Cada tema é uma prateleira da estante:
  - title: a situação que me leva até aquela prateleira, começando com "Quando", por exemplo "Quando busco pensar o Brasil a partir da negritude". No máximo 60 caracteres, sem ponto final, com verbos variados entre os temas.
  - text: um parágrafo breve que cite dois ou três livros da lista, com cada título citado entre asteriscos, exatamente como aparece na lista, como *Torto Arado*.
  - books: os números de todos os livros da lista que pertencem a esta prateleira. Cada livro em no máximo um tema; seja generoso, mas só quando a ligação for clara.

Responda apenas com JSON:
{{"lens": "...", "themes": [{{"title": "Quando ...", "text": "...", "books": [1, 2]}}]}}

Livros:
{books}"""


def book_list(books: list[dict]) -> str:
    lines = []
    for number, book in enumerate(books, start=1):
        title = book.get("ol_title") or book["title"]
        authors = ", ".join(book.get("authors") or [])
        lines.append(f"{number}. {title} — {authors}" if authors else f"{number}. {title}")
    return "\n".join(lines)


def parse_portrait(text: str, book_count: int) -> dict:
    """Reads the model's portrait; book numbers come 1-based and are returned as 0-based indexes."""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("portrait response has no JSON")
    data = json.loads(text[start : end + 1])
    lens = data.get("lens")
    if not isinstance(lens, str) or not lens.strip():
        raise ValueError("portrait response has no lens")
    themes, used = [], set()
    for theme in data.get("themes") or []:
        if not isinstance(theme, dict):
            continue
        title = str(theme.get("title") or theme.get("name") or "").strip()
        if not title:
            continue
        indexes = []
        for number in theme.get("books") or []:
            if isinstance(number, int) and 1 <= number <= book_count and number - 1 not in used:
                used.add(number - 1)
                indexes.append(number - 1)
        themes.append({"title": title, "text": str(theme.get("text", "")).strip(), "books": indexes})
    return {"lens": lens.strip(), "themes": themes}


def write_portrait(books: list[dict], api_key: str) -> tuple[dict, float]:
    text, cost = openrouter.complete(
        api_key, PROMPT.format(books=book_list(books)), max_tokens=4000, temperature=0.7
    )
    return parse_portrait(text, len(books)), cost
