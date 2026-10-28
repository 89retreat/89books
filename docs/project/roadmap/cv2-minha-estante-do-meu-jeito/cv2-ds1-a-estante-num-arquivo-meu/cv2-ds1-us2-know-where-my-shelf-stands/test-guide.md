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

A registrar depois da implementação e da validação do Navigator.
