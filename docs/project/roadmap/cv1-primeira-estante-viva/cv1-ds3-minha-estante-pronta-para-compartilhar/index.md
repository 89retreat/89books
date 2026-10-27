---
code: CV1.DS3
level: Delivery Story
status: Done
status_reason: US1, US2 e US3 validadas pelo Navigator e concluídas em 2026-10-27
updated: 2026-10-27
former_title: Do clone à estante
related:
  - ../index.md
---

[< CV1](../index.md)

# CV1.DS3 — Minha estante pronta para compartilhar

**Status:** Done

---

## Outcome

Uma pessoa do grupo clona o repositório, segue o guia de primeiros passos,
põe as fotos em `my-bookshelf/`, roda um comando e recebe a própria estante.
O comando cuida da configuração que falta, explicando como obter cada chave,
e avisa o custo antes de gastar. Toda a superfície do terminal é em inglês.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| [CV1.DS3.US1](cv1-ds3-us1-guided-setup/index.md) | Guided setup in the terminal | User Story | `uv run shelf` sem argumentos usa `my-bookshelf/`; se falta configuração, explica como obter cada chave, pede o nome da estante e as chaves (Google Books opcional), testa cada chave e grava; antes de reconhecer, mostra fotos, custo e tempo estimados e pede confirmação. | Done |
| [CV1.DS3.US2](cv1-ds3-us2-getting-started/index.md) | Getting started, from clone to shelf | User Story | Um guia em inglês leva do clone à estante: pré-requisitos (git, uv, acesso ao repositório, crédito no OpenRouter), a pasta `my-bookshelf/` já ignorada pelo git, fotos do iPhone em HEIC aceitas, onde fica a estante pronta e como compartilhá-la. | Done |
| [CV1.DS3.US3](cv1-ds3-us3-authors-by-known-name/index.md) | Authors by the name readers know | User Story | Cada lombada traz o autor pelo nome com que é conhecido (revisão do modelo) ou, na falta, por nome e sobrenome; nunca um sobrenome solto. | Done |

## Done Condition

O Navigator gera a própria estante partindo de um clone limpo, sem a
configuração local do projeto, seguindo só o guia e o terminal.
