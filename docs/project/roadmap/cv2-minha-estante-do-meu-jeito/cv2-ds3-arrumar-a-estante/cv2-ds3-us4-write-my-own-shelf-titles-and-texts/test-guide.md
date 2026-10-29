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

## Validation Evidence

A registrar depois da implementação e da validação do Navigator.
