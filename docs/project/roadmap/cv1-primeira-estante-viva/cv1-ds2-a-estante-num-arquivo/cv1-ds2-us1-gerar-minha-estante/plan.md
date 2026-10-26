[< Story](index.md)

# Plan — CV1.DS2.US1

## Objective

Transformar o spike num comando, `uv run shelf <folder>`, que entrega à
pessoa a estante como prêmio: um `shelf.html` autocontido com as fotos, os
livros e o retrato de si, mais um `books.yaml` com a lista.

## Pull

Puxada em 2026-10-26, logo depois do fechamento da CV1.DS1. Cadência
`accelerated`: o Navigator pediu "planeje e implemente".

## Prepare

- O spike (`spikes/reconhecimento/`) já tem extração por modelo de visão,
  busca na Open Library, deduplicação e o prompt do retrato validado com o
  Lula.
- Decisões: [stack](../../../../decisions/records/2026-10-26T1332Z-stack-e-hospedagem.md),
  [acesso e compartilhamento](../../../../decisions/records/2026-10-24T2013Z-acesso-do-grupo.md),
  [reconhecimento](../../../../decisions/records/2026-10-24T2013Z-reconhecimento-de-livros.md).
- Fotos reais para validação local: as 7 fotos de prateleira do Lula
  (consentimento registrado na TS1), fora do git.

## Scope

- Projeto Python na raiz (`pyproject.toml`, pacote `src/shelf/`), com
  `uv`, `pytest` e `ruff`, e o comando `shelf`. Por pedido do Navigator
  (2026-10-26), nomes de scripts, módulos, argumentos e instruções de uso
  ficam em inglês; a página da estante e o retrato, em português.
- Dependências: `httpx` (OpenRouter e Open Library), `Pillow` (fotos),
  `Jinja2` (template com escape automático), `PyYAML` (`books.yaml`).
- Módulos:
  - `config`: chave de `OPENROUTER_API_KEY` ou de `config.toml` na pasta
    (`openrouter_api_key`, `name` opcional); lista as fotos (`.jpg`,
    `.jpeg`, `.png`, `.webp`) em ordem de nome.
  - `photos`: corrige a rotação, reduz para no máximo 1600 px, regrava em
    JPEG sem EXIF e devolve um data URI.
  - `text`: normalização e similaridade de títulos, do spike.
  - `openrouter` e `recognition`: extraem livros de uma foto (Sonnet 5.5,
    `data_collection: deny`), com o prompt do spike.
  - `openlibrary`: liga cada livro à obra, com cache em `<folder>/.shelf/`.
  - `books`: deduplica e grava o `books.yaml`.
  - `portrait`: gera o retrato (lente e temas) em JSON.
  - `page`: renderiza o HTML a partir de `templates/shelf.html`.
  - `cli`: orquestra, informa progresso, livros e custo.
- O pipeline recebe as funções de rede por parâmetro, para os testes rodarem
  sem rede.
- `.gitignore` para `config.toml`, `.shelf/`, `shelf.html` e `books.yaml`.
- README e guia local com os comandos reais.

## Non-Goals

- Beleza, lombadas para livros sem capa e escolha da capa (US2).
- Ler o `books.yaml` editado, cache do reconhecimento por foto e
  `--new-portrait` (US3).
- Publicação no GitHub Pages (DS3).
- Apagar o spike: ele continua como registro da TS1.

## Acceptance Behavior

```text
Given uma pasta com fotos de estante ou prateleira e a chave do OpenRouter configurada
When rodo `uv run shelf <folder>`
Then recebo `shelf.html` e `books.yaml` dentro da pasta
And o HTML abre sozinho no navegador, sem internet além das capas, com as fotos, os livros e o retrato
And o HTML não contém a chave, caminhos locais nem EXIF das fotos
And o comando informa quantos livros reconheceu e quanto custou
```

```text
Given uma pasta sem fotos ou sem chave configurada
When rodo o comando
Then recebo uma mensagem clara do que falta, sem chamar o modelo
```

## Validation Route

- Automático: `uv run pytest` e `uv run ruff check .` passando. Os testes
  cobrem configuração e erros, fotos sem EXIF e reduzidas, deduplicação e
  `books.yaml`, leitura do retrato, escape e privacidade do HTML, e o
  pipeline de ponta a ponta com rede simulada.
- Driver: rodar com as 7 fotos do Lula numa pasta fora do repositório,
  conferir o HTML num navegador (computador e tamanho de celular) e procurar
  a chave e caminhos locais no arquivo.
- Navigator: rodar com fotos da própria estante, abrir o `shelf.html` no
  computador e no celular e reconhecer as fotos, os livros e o retrato.
  - Passa: o HTML abre sozinho, mostra os três e o retrato soa como você.
  - Falha: erro sem mensagem clara, HTML quebrado no celular, livros ou
    retrato ausentes, ou dado privado no arquivo.

E2E decision: o teste de ponta a ponta automatizado usa rede simulada; a
execução real com fotos é a rota do Driver e do Navigator.

## Implementation Contract

- TDD: testes antes do código em cada módulo com comportamento.
- Use uv run for Python commands and tests.
- Nenhuma foto, estante gerada ou chave entra no git.
- Commit só com arquivos da story; mensagem em inglês explicando o porquê.
  Sem push sem comando do Navigator.

## Stop Conditions

- scope_change_detected
- plan_rule_conflict
- failing_required_check_without_clear_fix
- navigator_decision_needed

## Approval Gate

- active checkpoint: `after_plan`
- pending confirmation: `navigator_approval`, satisfeita pela autoridade de
  plano da cadência `accelerated` (2026-10-26).
