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

## Automated Evidence — 2026-10-29

- `uv run ruff check .` — passed.
- `uv run ruff format --check .` — passed, 236 files formatted.
- `uv run pytest` — 201 passed.
- E2E gratuito em `/tmp/89books-ds3-us3-validation`: com seis fotos, a quarta
  escolha chegou primeiro como `[4, 1, 2, 3, 5, 6]`; depois a segunda chegou
  como `[2, 1, 3, 4, 5, 6]`, embora `config.toml` ainda apontasse para a
  primeira. A sexta permaneceu marcada como somente desktop, deixando a
  escolhida entre as cinco fotos móveis.
- `cover_photo: missing.jpg` fez `check` e `draw` saírem com erro 2 e preservou
  bytes da página, marcador e nomes do histórico. A escolha válida foi então
  restaurada e `check` voltou a passar.
- Captura desktop verificada em
  `/tmp/89books-ds3-us3-validation/desktop.png`.

## Navigator Evidence

O Navigator abriu a fixture, mudou `cover_photo` e redesenhou por `check`,
`draw` e `open`. Em 2026-10-29, informou que a validação deu certo; o aceite
foi registrado sem qualquer serviço pago ou leitura de histórico real.
