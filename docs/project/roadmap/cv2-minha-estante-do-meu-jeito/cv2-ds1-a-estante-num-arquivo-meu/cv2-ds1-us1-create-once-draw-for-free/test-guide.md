[< Story](index.md)

# Test Guide — CV2.DS1.US1 Create once, draw for free

## Automated Validation

```bash
uv run pytest tests/test_core.py tests/test_shelf_file.py tests/test_cli.py tests/test_main.py tests/test_page.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Cobrir criação nova, migração da CV1 sem reconhecimento ou catálogos, recusa
de sobrescrita, confirmação de custo, desenho sem chave/rede, proteção da
página em qualquer falha, abertura no navegador e comando sem verbo sem gasto.

## Navigator Validation

Em uma cópia descartável de uma estante CV1:

```bash
uv run shelf create --folder <cópia>
uv run shelf draw --folder <cópia>
uv run shelf open --folder <cópia>
```

Editar uma frase de `lens`, desenhar novamente e abrir no computador e no
celular. Depois introduzir um erro no YAML e confirmar a linha indicada e que
a página anterior continua idêntica.

Passa quando `books.yaml` é reutilizado sem releitura de fotos ou catálogos,
`draw` não pede chave nem gasta, a edição aparece e nenhum erro substitui a
página. Falha com gasto implícito, perda, releitura, edição ignorada ou erro
sem linha.

## Validation Evidence

A registrar depois da implementação e da validação do Navigator.
