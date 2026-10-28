[< Story](index.md)

# Test Guide — CV2.DS1.TS2 shelf.yaml, version 1

## Automated Validation

```bash
uv run pytest tests/test_shelf_file.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

O teste dedicado é a especificação executável do formato versão 1: campos,
ordem, valores opcionais, round trip, sintaxe, versão, chaves duplicadas,
campos desconhecidos, campos obrigatórios, tipos e coleção de vários erros com
linhas e caminhos.

## Navigator Validation

Não requerida; as evidências automatizadas definidas no plano são o aceite
desta Technical Story.

## Validation Evidence

A registrar depois da implementação.
