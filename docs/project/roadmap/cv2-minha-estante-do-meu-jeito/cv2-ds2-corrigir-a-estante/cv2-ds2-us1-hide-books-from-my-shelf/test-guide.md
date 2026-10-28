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

A registrar depois da implementação e da validação do Navigator.
