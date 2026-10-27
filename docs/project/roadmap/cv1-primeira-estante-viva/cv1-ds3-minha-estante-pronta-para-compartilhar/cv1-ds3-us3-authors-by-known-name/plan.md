[< Story](index.md)

# Plan — CV1.DS3.US3

## Objective

Nenhuma lombada com sobrenome solto: o autor aparece pelo nome com que os
leitores o conhecem, dito pelo modelo, ou por nome e sobrenome, por uma regra
local.

## Pull

Feedback recebido pelo Navigator depois de validar a DS3: os sobrenomes
soltos incomodam. A regra atual (US3 da DS2) corta para o sobrenome todo nome
com mais de 16 caracteres; na estante do Lula, 43 de 130 autores.

## Approval

Abordagem aprovada pelo Navigator em 2026-10-27 ("aprovo, pode seguir"),
como uma nova story na DS3, com teste barato sobre o reconhecimento já salvo
do Lula. O plano abaixo detalha essa abordagem sem ampliá-la.

## Scope

- **Revisão:** o prompt passa a pedir também `known_as`, um mapa de cada
  autor da estante (inclusive os corrigidos) para o nome com que é conhecido,
  com até 24 caracteres; para instituições, um nome curto. Mesma chamada.
- **Regra local** (`shelves.short_name`): caixa alta vira nome próprio; tira
  títulos (Dom, Frei, Padre, Dr.); até o limite, o nome inteiro; acima,
  primeiro nome + partícula + último sobrenome + sufixo.
- **Lombada:** usa o `known_as` do primeiro autor quando cabe no limite;
  senão, a regra. O limite sobe de 16 para 24 caracteres, conferido no
  navegador.
- **`books.yaml`:** grava `known_as` ao lado de `authors`.
- **"Quem mais mora aqui"** usa o mesmo nome da lombada.

## Non-Goals

- Correção manual de nomes (CV2.DS1.US1).
- Uma segunda chamada ao modelo só para nomes.

## Validation Route

- Automático: `uv run pytest`, `uv run ruff check . && uv run ruff format --check .`.
  Testes novos: a regra (caixa alta, títulos, partículas, sufixos, nunca
  sobrenome solto); `parse_review` lê `known_as` e tolera a falta dele; a
  lombada prefere o `known_as`; o pipeline grava `known_as`.
- Driver: só a revisão do modelo sobre os livros já salvos do Lula
  (~US$ 0,05), depois o antes e depois dos nomes e uma olhada nas lombadas no
  navegador. Sem refazer o reconhecimento.
- Navigator: abrir a estante do Lula re-renderizada.
  - Passa: nenhuma lombada com sobrenome solto, e os nomes cabem.
  - Falha: um sobrenome solto, um nome errado que antes estava certo, ou um
    nome que não cabe na lombada.

E2E decision: rede simulada nos testes; a revisão real sobre os livros do
Lula é a rota real.

## Implementation Contract

- TDD em `shelves`, `review`, `books` e `cli`.
- Use uv run for Python commands and tests.
- Nenhuma foto, estante gerada ou chave entra no git.
- Commit só com arquivos da story; mensagem em inglês explicando o porquê.

## Stop Conditions

- scope_change_detected
- plan_rule_conflict
- failing_required_check_without_clear_fix
- navigator_decision_needed
