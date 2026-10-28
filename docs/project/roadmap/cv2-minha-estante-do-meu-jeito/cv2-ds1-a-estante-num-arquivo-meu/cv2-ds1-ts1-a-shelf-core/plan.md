[< Story](index.md)

# Plan — CV2.DS1.TS1

## Objective

Separar o núcleo da estante do terminal, sem mudar o que a pessoa vê:
`generate` devolve a estante como dados e `draw` devolve o HTML; o comando só
pergunta, confirma, mostra e grava.

## Pull

Puxada em 2026-10-28, depois do push da reescrita da CV2. É a primeira story
da CV2: a TS2 (`shelf.yaml`) e as US1 a US3 (`create`, `draw`, painel,
versões) se apoiam em `generate` e `draw` separados.

## Prepare

- Hoje `cli.build_shelf` faz tudo: carrega a configuração já lida, cria os
  catálogos sobre a pasta `.shelf/`, reconhece, consulta, revisa, escreve o
  retrato, desenha e grava `shelf.html` e `books.yaml`, imprimindo cada passo.
- As peças já são injetáveis (`recognize`, `library`, `review`, `portrait`,
  `covers`, `second`, `log`, `progress`); falta tirar a gravação e as
  decisões de pasta de dentro do pipeline.
- A revisão aceita duas formas de resposta (`*rest`), débito adiado ao fechar
  a CV1.DS3.
- Princípio de produto preservado: "Gastar é sempre uma escolha". O núcleo não
  confirma gasto; quem confirma é o terminal, antes de chamar `generate`.

## Scope

- **`src/shelf/core.py`**:
  - `Shelf` (dataclass): `name`, `photos` (nomes dos arquivos), `books`,
    `left_out`, `portrait`, `cost`;
  - `Services` (dataclass): `recognize`, `review`, `portrait`, `library`,
    `second`, `covers`;
  - `generate(photos: list[Path], api_key, name, services, log, progress) -> Shelf`:
    o pipeline atual, sem `render` nem gravação; salva só os caches que os
    serviços recebem;
  - `draw(shelf: Shelf, images: list[str]) -> str`: o HTML, via `page.render`.
- **`cli`**: `build_shelf(config, ...)` vira uma função fina que monta os
  `Services` sobre `.shelf/`, chama `generate`, prepara as imagens, chama
  `draw` e grava `shelf.html` e `books.yaml`; mensagens e `Result` iguais.
- **`review.review_books`** e os fakes dos testes devolvem sempre três valores.
- **Núcleo e terminal**: tudo que decide a estante fica em `core`; `cli` e
  `setup` só falam com a pessoa e com o disco.

## Non-Goals

- `shelf.yaml`, comandos novos, versões em `history/`.
- Qualquer mudança de comportamento visível.

## Acceptance Behavior

Ver o [índice da story](index.md).

## Validation Route

- Automático: `uv run pytest`, `uv run ruff check . && uv run ruff format --check .`.
  Testes novos: `generate` com serviços falsos devolve livros, retrato e
  custo sem criar `shelf.html` nem `books.yaml`; `draw` devolve o HTML sem
  serviços; o teste de arquitetura sobre `core`. Os testes existentes de
  `build_shelf` e `main` continuam passando sem mudança de expectativa.
- Driver: `uv run shelf` real numa pasta com uma foto só (cerca de US$ 0,03),
  conferindo que as mensagens e os arquivos gerados são os mesmos de antes.
- Navigator: revisar a fronteira entre `core` e `cli` no diff.
  - Passa: o comando funciona como antes, e `core` não fala com o terminal.
  - Falha: uma mudança no que a pessoa vê, ou lógica de produto que ficou em
    `cli`.

E2E decision: testes com serviços falsos e uma rodada real com uma foto.

## Implementation Contract

- TDD: escrever primeiro os testes de `core` e o de arquitetura.
- Use uv run for Python commands and tests.
- Nenhuma foto, estante gerada ou chave entra no git.
- Commit só com arquivos da story; mensagem em inglês explicando o porquê.

## Stop Conditions

- scope_change_detected
- plan_rule_conflict
- failing_required_check_without_clear_fix
- navigator_decision_needed

## Approval Gate

- active checkpoint: `after_plan`
- pending confirmation: `navigator_approval`
