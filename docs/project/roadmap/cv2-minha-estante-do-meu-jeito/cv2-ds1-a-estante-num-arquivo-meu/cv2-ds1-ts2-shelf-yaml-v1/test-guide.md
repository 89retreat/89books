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

2026-10-28, Driver:

- `uv run pytest tests/test_shelf_file.py`: 11 testes passando.
- `uv run pytest`: 117 testes passando.
- `uv run ruff check . && uv run ruff format --check .`: limpo.
- O teste de arquitetura falhou, como devia, quando um `import pathlib` e,
  separadamente, um `print` foram acrescentados de propósito ao módulo.
- O round trip preserva `face: false`, `hidden: false`, `cover: none`, capas em
  URL, textos multilinha e proveniência; o dumper produz saída idêntica depois
  da segunda rodada.
- Um arquivo com oito problemas devolveu os oito, ordenados por linha e com
  caminhos como `shelves[0].books[1].authors`; nenhum documento parcial foi
  retornado.
- Aceite automático conforme a política permanente de Technical Stories
  aprovada pelo Navigator em 2026-10-28.
