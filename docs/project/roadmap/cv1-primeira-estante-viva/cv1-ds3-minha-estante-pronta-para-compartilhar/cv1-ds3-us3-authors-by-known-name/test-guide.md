[< Story](index.md)

# Test Guide — CV1.DS3.US3

## Automated Validation

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Testes novos: `short_name` (caixa alta, títulos, partículas, sufixos, nunca
sobrenome solto); `long_names` lista só os primeiros autores com mais de 24
caracteres; `parse_names` lê `known_as` par a par, inclusive de resposta
cortada; `name_books` grava `known_as`; a lombada prefere o `known_as` quando
cabe e fica mais larga para nomes longos; o pipeline leva o nome até a
página e o `books.yaml`.

## E2E Decision

Rede simulada nos testes; a revisão real sobre os livros já salvos do Lula
e a página re-renderizada são a rota real.

## Navigator Validation

Abrir `~/Downloads/estante-lula-nomes.html`.

Passa: nenhuma lombada com sobrenome solto, e os nomes cabem sem esconder o
título. Falha: um sobrenome solto, um nome errado que antes estava certo, ou
um nome que esconde o título.

## Validation Evidence

2026-10-27, Driver, sobre os 160 livros já salvos do Lula, sem refazer o
reconhecimento:

- `uv run pytest`: 98 testes passando. `ruff` limpo.
- Primeira tentativa (US$ 0,11): o prompt pedia o nome de todos os autores;
  a resposta veio cortada no meio da lista e nenhum nome foi lido. O prompt
  passou a perguntar só pelos nomes longos, e a leitura passou a aproveitar
  os pares que chegam.
- Segunda tentativa (US$ 0,047): 6 nomes longos, todos respondidos, como
  "Ana Fani A. Carlos", "Leôncio M. Rodrigues" e "Seminário Fazendo Gênero".
- Dos 43 autores que antes viravam sobrenome solto, nenhum continua assim:
  37 pela regra (o nome inteiro cabe até 24 caracteres: "Carolina Maria de
  Jesus", "Luis Fernando Verissimo") e 6 pelo modelo.
- No navegador, a 1280 px, os nomes longos ocupavam a lombada inteira e
  escondiam o título; passaram a quebrar em colunas, com a lombada mais
  larga. Nas 104 lombadas visíveis, o título tem ao menos 58 px.
