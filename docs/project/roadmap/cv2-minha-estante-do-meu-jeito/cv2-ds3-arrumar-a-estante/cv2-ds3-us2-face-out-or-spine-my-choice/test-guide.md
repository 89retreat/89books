[< Story](index.md)

# Test Guide — CV2.DS3.US2 Face out or spine, my choice

## Automated Validation

```bash
uv run pytest tests/test_core.py tests/test_shelves.py tests/test_page.py tests/test_cli.py tests/test_shelf_file.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Cobrir `true`, `false`, ausência automática, falta de capa, `cover: none`,
hidden, operação pura tri-state, criação sem escolha automática materializada
e várias faces em ordem.

## Navigator Validation

Em `/tmp/89books-ds3-us2-validation`:

1. observar livro automático citado, capa explícita não citada e lombada
   explícita citada;
2. observar `face: true` com `cover: none` cair para lombada;
3. confirmar várias capas quebrando em fileiras sem sobreposição;
4. remover uma marca `face`, redesenhar e confirmar retorno ao automático;
5. confirmar redraw gratuito e snapshot sem ler versões.

## Validation Evidence

A registrar depois da implementação e da validação do Navigator.
