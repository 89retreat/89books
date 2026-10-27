---
code: CV1.DS3.US2
level: User Story
status: Active
status_reason: puxada após a US1; plano aguarda aprovação do Navigator
updated: 2026-10-27
related:
  - ../index.md
  - ../cv1-ds3-us1-guided-setup/index.md
---

[< Parent](../index.md)

# CV1.DS3.US2 — Getting started, from clone to shelf

**Status:** Active
**Type:** User Story

---

## User Story

As uma pessoa do grupo que recebeu o link do repositório,
I want um guia curto que me leve do clone à minha estante,
So that eu faça tudo sozinha, inclusive com as fotos que tirei no iPhone.

## Outcome

Um `GETTING_STARTED.md` em inglês, ligado no topo do README, leva do zero à
estante: pré-requisitos, clone, fotos em `my-bookshelf/` (que já existe no
clone, com um aviso de privacidade), `uv run shelf`, onde está a estante
pronta e como compartilhá-la. Fotos HEIC do iPhone funcionam. O terminal
aponta o próximo passo quando a pasta está vazia e, no fim, onde abrir a
estante.

## Acceptance Behavior

```text
Given a fresh clone
When I follow GETTING_STARTED.md
Then my-bookshelf/ is already there, and git ignores anything I put in it
And I learn what I need before starting: git, uv, access to the repository and some OpenRouter credit
```

```text
Given photos taken on an iPhone (.heic)
When I run `uv run shelf`
Then they are read like any other photo
```

```text
Given an empty my-bookshelf/
When I run `uv run shelf`
Then I am told to add photos, before any key is asked
```

```text
Given a finished shelf
When the command ends
Then it tells me where shelf.html is and how to open and share it
```

## Out Of Scope

- Publicar por link (CV2.DS2) e corrigir a estante (CV2.DS1).
- Instalar `git` ou `uv` pela pessoa: o guia aponta como.
