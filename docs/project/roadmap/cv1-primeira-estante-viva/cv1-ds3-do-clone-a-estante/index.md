---
code: CV1.DS3
level: Delivery Story
status: Active
status_reason: criada na reorganização de 2026-10-27; US1 a seguir
updated: 2026-10-27
related:
  - ../index.md
---

[< CV1](../index.md)

# CV1.DS3 — Do clone à estante

**Status:** Active

---

## Outcome

Uma pessoa do grupo clona o repositório, segue o guia de primeiros passos,
põe as fotos em `my-bookshelf/`, roda um comando e recebe a própria estante.
O comando cuida da configuração que falta, explicando como obter cada chave,
e avisa o custo antes de gastar. Toda a superfície do terminal é em inglês.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| CV1.DS3.US1 | Guided setup in the terminal | User Story | `uv run shelf` sem argumentos usa `my-bookshelf/`; se falta configuração, explica como obter cada chave, pede o nome da estante e as chaves (Google Books opcional), testa cada chave e grava; antes de reconhecer, mostra fotos, custo e tempo estimados e pede confirmação. | Planned |
| CV1.DS3.US2 | Getting started, from clone to shelf | User Story | Um guia em inglês leva do clone à estante: pré-requisitos (git, uv, acesso ao repositório, crédito no OpenRouter), a pasta `my-bookshelf/` já ignorada pelo git, fotos do iPhone em HEIC aceitas, onde fica a estante pronta e como compartilhá-la. | Planned |

## Done Condition

O Navigator gera a própria estante partindo de um clone limpo, sem a
configuração local do projeto, seguindo só o guia e o terminal.
