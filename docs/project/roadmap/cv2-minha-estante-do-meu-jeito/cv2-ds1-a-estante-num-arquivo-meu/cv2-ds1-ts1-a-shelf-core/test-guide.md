[< Story](index.md)

# Test Guide — CV2.DS1.TS1

## Automated Validation

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

`tests/test_core.py`: `generate` com serviços falsos devolve livros, retrato e
custo sem criar arquivo na pasta; reporta pelo `log` que recebe e fica em
silêncio sem ele; `draw` devolve a página sem serviço nenhum; o teste de
arquitetura lê `core.py` e falha se ele chamar `print` ou `input`, ou importar
`sys`, `os`, `getpass`, `shelf.cli`, `shelf.setup`, `shelf.progress` ou
`shelf.config`. Os testes de `build_shelf` e `main` seguem com as mesmas
expectativas; os fakes de revisão passaram a devolver três valores.

## E2E Decision

Testes com serviços falsos e uma rodada real com uma foto.

## Navigator Validation

Revisar no diff a fronteira entre `src/shelf/core.py` e `src/shelf/cli.py`.

Passa: o comando funciona como antes e o núcleo não fala com o terminal.
Falha: algo mudou para quem usa o comando, ou uma regra de produto ficou no
`cli`.

## Validation Evidence

2026-10-28, Driver:

- `uv run pytest`: 106 testes passando. `ruff` limpo.
- O teste de arquitetura falhou, como devia, ao acrescentar de propósito um
  `import sys` e, depois, um `print` ao `core.py`.
- `uv run shelf shelf --yes` real, fora do repositório, com uma foto do Lula
  (US$ 0,03): as mesmas mensagens na mesma ordem de antes, `shelf.html` e
  `books.yaml` gravados, nome na página, nenhum caminho local no HTML. A pasta
  foi apagada depois.
- A revisão do modelo devolve sempre `(entries, cost, names)`; saiu o `*rest`
  do pipeline, débito adiado no fechamento da CV1.DS3.
