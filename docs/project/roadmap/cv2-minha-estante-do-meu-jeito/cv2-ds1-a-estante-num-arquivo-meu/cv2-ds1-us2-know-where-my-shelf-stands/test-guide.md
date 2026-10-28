[< Story](index.md)

# Test Guide — CV2.DS1.US2 Know where my shelf stands

## Automated Validation

```bash
uv run pytest tests/test_status.py tests/test_main.py tests/test_shelf_file.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Cobrir os cinco estados, contagens, datas, versões, próximo verbo, validação
com todos os erros, resolução da pasta e ausência total de I/O no núcleo ou de
chamadas pagas no painel e em `check`.

## Navigator Validation

Usar `/tmp/estante-alisson-validacao-us1` sem chaves: painel pronto, `check`
válido, painel stale depois de editar, resumo + detalhes com dois erros,
restauração e teste da pasta atual versus fallback `my-bookshelf/`.

Passa quando caminho, estados, contagens, horários e próximo comando batem com
os arquivos, todos os erros têm linha e nada é alterado ou gasto. Falha com
pasta surpreendente, recomendação errada, setup/gasto, erro sem linha ou
qualquer byte modificado.

## Validation Evidence

### Automated — passed

- `uv run pytest`: 137 passed.
- `uv run ruff check . && uv run ruff format --check .`: passed.
- The pure status core has no filesystem, environment, terminal or clock access.

### Driver E2E — passed

With API keys removed, `/tmp/estante-alisson-validacao-us1` showed 1 photo,
11 books, edit/draw times, zero versions and `open`. Touching `shelf.yaml`
changed the recommendation to `draw`. Two YAML errors produced a two-error
summary and line-specific `check` output with exit 2 while the previous page
hash survived. Restoring the source and drawing again was free. Running from a
shelf directory selected the current directory; running from the repository
root selected `my-bookshelf/`.

### Navigator — pending

Confirm that the panel is understandable, `check` is useful and the folder
selection rule is unsurprising.
