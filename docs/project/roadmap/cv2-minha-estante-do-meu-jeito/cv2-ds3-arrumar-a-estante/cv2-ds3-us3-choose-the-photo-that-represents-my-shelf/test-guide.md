[< Story](index.md)

# Test Guide — CV2.DS3.US3 Choose the photo that represents my shelf

## Automated Validation

```bash
uv run pytest tests/test_core.py tests/test_config.py tests/test_cli.py tests/test_page.py tests/test_shelves.py tests/test_main.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Cobrir operação pura, ordenação estável, validação compartilhada de ativos,
autoridade de `shelf.yaml` sobre configuração legada, preservação durante
`recreate`, segurança atômica e primeira posição no mosaico.

## Navigator Validation

Em `/tmp/89books-ds3-us3-validation`:

1. escolher pelo nome uma foto que não seja a primeira alfabeticamente;
2. rodar `check`, `draw` e `open` sem chave e observar o destaque;
3. conferir a ordem das demais em desktop e a presença da escolhida no celular;
4. trocar a escolha e confirmar que só o destaque muda;
5. usar temporariamente um nome ausente e confirmar que `check`/`draw` falham
   sem substituir a página anterior;
6. restaurar uma escolha válida e redesenhar gratuitamente.

**Esperado:** `cover_photo` é a única decisão de destaque depois que a fonte
existe. **Passa:** escolha visível, ordem estável, erro seguro e zero custo.
**Falha:** ordem alfabética ou `config.toml` vence, a escolhida some no celular,
a página é substituída em erro ou surge qualquer pedido de chave/pagamento.

## Validation Evidence

A registrar depois da implementação e da validação do Navigator.
