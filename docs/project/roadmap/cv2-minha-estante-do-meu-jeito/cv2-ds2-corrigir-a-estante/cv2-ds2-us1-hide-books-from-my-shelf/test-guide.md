[< Story](index.md)

# Test Guide — CV2.DS2.US1 Hide books from my shelf

## Automated Validation

```bash
uv run pytest tests/test_core.py tests/test_page.py tests/test_shelves.py tests/test_shelf_file.py tests/test_cli.py tests/test_status.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Cobrir ausência de capa/lombada e autor frequente, `false`/ausente visível,
ordem estável, prateleira vazia, operações puras imutáveis, contagens,
histórico e ausência de chave/rede.

## Navigator Validation

Numa cópia descartável, escolher um livro, adicionar `hidden: true`, rodar
`check`, `draw`, painel e `open`; confirmar 11 total, 10 visíveis, 1 escondido
e o livro ausente. Remover a linha, desenhar e abrir; confirmar o retorno na
mesma prateleira. `history` lista snapshots apenas por metadados.

A fixture automatizada valida “Quem mais mora aqui” se a estante escolhida não
oferecer um autor frequente adequado.

## Validation Evidence

### Automated — passed

- `uv run pytest`: 163 passed.
- `uv run ruff check . && uv run ruff format --check .`: passed.
- Pure hide/show operations return copies and preserve all book metadata.
- Page fixtures cover frequent authors, false/absent visibility, order and an
  authored shelf with every book hidden.

### Driver E2E — passed

A free synthetic shelf with two books and one shared author was drawn with one
book hidden. `check` reported 2 total/1 visible; draw rendered 1 book and saved
a version; status reported 2 total/1 visible/1 hidden. The hidden title, cover
and frequent-author surface were absent. Removing the mark saved a second
version, rendered both books and restored “Quem mais mora aqui”. No keys or
network were available.

### Navigator — passed

The Navigator hid one book in `/tmp/estante-alisson-hide-us1`. `check` showed
11 total and 10 visible; draw saved `shelf-2026-10-28-1805.yaml` and rendered
10 books. Opening the page confirmed the book disappeared without breaking the
shelf. The Navigator removed the mark, drew again and confirmed that the book
returned.
