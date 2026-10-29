[< Story](index.md)

# Test Guide — CV2.DS3.US4 Write my own shelf titles and texts

## Automated Validation

```bash
uv run pytest tests/test_core.py tests/test_page.py tests/test_shelves.py tests/test_shelf_file.py tests/test_cli.py tests/test_history.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Cobrir operações puras, conteúdo literal, escape antes do itálico, campos
vazios, citação como entrada da composição automática, precedência de `face`,
semântica de fechamento, fluxo gratuito, snapshot e restore descartável.

## Navigator Validation

Em `/tmp/89books-ds3-us4-validation`:

1. editar abertura, título e texto com asteriscos e tags aparentes;
2. rodar `check`, `draw` e `open` sem chave;
3. confirmar itálico somente na abertura/parágrafo, tags como texto seguro e
   asteriscos literais no título;
4. confirmar que a citação muda apenas a face automática, sem reordenar livros;
5. marcar a face explicitamente e confirmar que ela vence o texto; remover a
   marca para voltar ao automático;
6. restaurar uma versão descartável e redesenhar para recuperar a linguagem
   anterior.

**Esperado:** a página usa as palavras exatas da pessoa com escape seguro.
**Passa:** conteúdo, itálico, faces, ordem e restore corretos, sem custo.
**Falha:** texto gerado vence, HTML executa, título interpreta markup, livros
mudam de ordem, escolha explícita é ignorada ou algum serviço pago é chamado.

## Automated Evidence — 2026-10-29

- `uv run ruff check .` — passed.
- `uv run ruff format --check .` — passed, 244 files formatted.
- `uv run pytest` — 206 passed.
- E2E gratuito em `/tmp/89books-ds3-us4-validation`: abertura e texto
  converteram pares simples em itálico; título manteve asteriscos literais;
  `<segura>` e `<script>não executar</script>` apareceram como texto seguro; a
  citação mudou a face automática de Torto Arado para Cynefin sem reordenar os
  livros.
- `face: false` em Cynefin venceu a citação; remover a linha restaurou o
  automático. Uma versão inicial foi restaurada, redesenhada e depois a versão
  autoral voltou por `restore`, sempre sem chave, rede ou custo.
- Captura visual verificada em
  `/tmp/89books-ds3-us4-validation/authored.png`.

## Navigator Evidence

A captura fornecida pelo Navigator em 2026-10-29 confirmou `voz` e `Cynefin`
em itálico, asteriscos literais no título, `<segura>`, `<autoral>` e `<script>`
visíveis como texto inerte, Torto Arado primeiro e a capa azul de Cynefin de
frente. O Navigator declarou a história validada e autorizou o fechamento; as
transições de `face: false` e restore ficaram cobertas pelo E2E offline.
