[< Story](index.md)

# Test Guide — CV1.DS2.US1

## Automated Validation

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Os testes rodam sem rede (OpenRouter e Open Library simulados) e cobrem:
configuração e mensagens de erro, fotos reduzidas e sem EXIF, normalização de
títulos, deduplicação e `books.yaml`, leitura das respostas do modelo, escape
do HTML e o pipeline de ponta a ponta, conferindo que a página não contém a
chave, caminhos locais nem EXIF.

## E2E Decision

Ponta a ponta automatizado com rede simulada. A execução real com fotos é
manual, pelo Driver e pelo Navigator, porque custa dinheiro e usa fotos
pessoais.

## Navigator Validation

1. Ponha fotos da sua estante numa pasta e a chave em `config.toml` ou em
   `OPENROUTER_API_KEY` (ver o `README.md`).
2. Rode `uv run shelf <pasta>`.
3. Abra o `shelf.html` no computador e mande o arquivo para o seu celular.

Observação esperada: o comando informa livros e custo; a página mostra as
fotos num carrossel, a lente, os temas e os livros.

Passa: a página abre sozinha nos dois aparelhos e o retrato soa como você.
Falha: erro sem mensagem clara, página quebrada no celular, livros ou retrato
ausentes, ou dado privado no arquivo.

## Validation Evidence

2026-10-26, Driver:

- `uv run pytest`: 20 testes passando. `ruff check` e `ruff format --check`
  limpos.
- Execução real com as 7 fotos de prateleira do Lula numa pasta fora do
  repositório: 161 livros, 108 com obra na Open Library e 58 com capa;
  US$ 0,09; cerca de 6 minutos, quase todos nas buscas da Open Library.
- `shelf.html` com 1,4 MB: sem a chave, sem caminhos locais, as 7 fotos sem
  EXIF. Conferido no navegador em 1280 px e em 390 px de largura.
- Retrato com a lente e seis temas; o prompt pede de três a cinco.

2026-10-26, Navigator: validou a estante gerada com as fotos do Lula, no
computador e no celular, em vez de rodar o comando com a própria estante.
Os pontos de design levantados (carrossel pouco visível, lista longa demais)
viraram o escopo da US2, desenhado em protótipos e aprovado.
