[< Story](index.md)

# Test Guide — CV2.DS2.US2 Fix titles, authors and covers

## Automated Validation

```bash
uv run pytest tests/test_core.py tests/test_shelves.py tests/test_page.py tests/test_cli.py tests/test_main.py tests/test_photos.py tests/test_shelf_file.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Cobrir identidade corrigida, `known_as` literal, operações puras, HTTPS sem
fetch, `none`, capa local embutida sem EXIF/caminho, confinamento, symlink,
extensão, ausência, limites 5 MiB/25 MP e preservação atômica em erro.

## Navigator Validation

Numa cópia descartável:

1. corrigir o livro identificado errado e confirmar título/autor/nome na página;
2. usar `cover: none` num livro de frente e observar lombada;
3. usar uma pequena capa local e observar a capa voltar;
4. confirmar snapshot, zero chave/rede/custo e HTML sem caminho local.

URL HTTPS e limites usam fixtures automatizadas, sem download nem arquivo
gigante real.

## Validation Evidence

A registrar depois da implementação e da validação do Navigator.
