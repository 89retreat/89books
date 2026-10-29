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

## Automated Evidence — 2026-10-29

- `uv run ruff check .` — passed.
- `uv run ruff format --check .` — passed, 228 files formatted.
- `uv run pytest` — 195 passed.
- E2E gratuito em `/tmp/89books-ds3-us2-validation`: automático e `true`
  produziram duas capas; `false` e `cover: none` produziram lombadas; seis
  escolhas adicionais chegaram em ordem à seção “Muitas capas”; nove imagens
  locais foram incorporadas sem rede.

## Navigator Evidence

Pendente: abrir a fixture, confirmar as quatro precedências na primeira seção
e observar que as seis capas da segunda seção quebram em fileiras sem
sobreposição. Depois, remover `face: true` de “Capa forçada” para confirmar o
retorno ao automático.
