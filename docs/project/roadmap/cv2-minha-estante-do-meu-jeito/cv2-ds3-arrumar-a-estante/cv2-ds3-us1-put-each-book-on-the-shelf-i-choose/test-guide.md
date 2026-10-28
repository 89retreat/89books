[< Story](index.md)

# Test Guide — CV2.DS3.US1 Put each book on the shelf I choose

## Automated Validation

```bash
uv run pytest tests/test_core.py tests/test_shelves.py tests/test_page.py tests/test_cli.py tests/test_shelf_file.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Cobrir ordem literal de livros/seções, seção final customizada regular,
fechamento canônico, operações puras imutáveis, metadata completa, posições e
remoção segura de seção vazia.

## Navigator Validation

Em `/tmp/89books-ds3-us1-validation`:

1. mover um bloco completo para outra seção e para uma posição escolhida;
2. criar uma seção final sem texto e confirmar que ela continua regular;
3. reordenar essa seção;
4. esvaziá-la, removê-la e redesenhar;
5. confirmar redraw gratuito e novas entradas de histórico sem ler versões.

## Validation Evidence

A registrar depois da implementação e da validação do Navigator.
