---
code: CV1.DS3.US1
level: User Story
status: Active
status_reason: implementada e validada pelo Driver num clone limpo; validação do Navigator junto com a US2
updated: 2026-10-27
related:
  - ../index.md
---

[< Parent](../index.md)

# CV1.DS3.US1 — Guided setup in the terminal

**Status:** Active
**Type:** User Story

---

## User Story

As uma pessoa do grupo que acabou de clonar o repositório,
I want rodar um comando só e ser guiada pelo que falta configurar,
So that eu chegue à minha estante sem ler código, sem editar arquivos de
configuração e sem descobrir o custo depois de gastar.

## Outcome

`uv run shelf`, sem argumentos, trabalha na pasta `my-bookshelf/`. Quando
falta configuração, o comando explica em inglês como obter cada chave, pede o
nome que aparece na estante e as chaves, testa cada chave e grava tudo em
`my-bookshelf/config.toml`. Antes de reconhecer as fotos, mostra quantas são,
o custo e o tempo estimados e pede confirmação.

## Acceptance Behavior

```text
Given a fresh clone with photos in my-bookshelf/ and no configuration
When I run `uv run shelf`
Then it explains how to get an OpenRouter key, asks for it, checks it and tells me the balance
And it asks for my name, as shown on the shelf, and for an optional Google Books key, which I can skip
And it saves my answers to my-bookshelf/config.toml, which git ignores
And it shows the number of photos, the estimated cost and time, and asks me to confirm before spending
```

```text
Given a key that OpenRouter rejects
When I paste it during setup
Then I am told it did not work and asked again, before any photo is read
```

```text
Given a configured folder
When I run `uv run shelf` again
Then it asks nothing but the cost confirmation, and `--yes` skips that too
```

## Out Of Scope

- O guia de primeiros passos, fotos HEIC e a criação de `my-bookshelf/` no
  repositório (CV1.DS3.US2).
- Correção da estante e novo retrato (CV2.DS1).
