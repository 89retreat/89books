---
code: CV2.DS2.US1
level: User Story
status: Active
status_reason: puxada em 2026-10-28; aguarda preparação e plano aprovado pelo Navigator
updated: 2026-10-28
related:
  - ../index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/cv2-ds1-us3-never-lose-an-edit/index.md
---

[< Parent](../index.md)

# CV2.DS2.US1 — Hide books from my shelf

**Status:** Active
**Type:** User Story

---

## User Story

In order to a estante mostrar apenas o que quero mostrar,
As uma pessoa que revisa a própria estante,
I want esconder um livro sem apagá-lo do meu arquivo,
So that posso trazê-lo de volta quando quiser e preservar meu histórico.

## Outcome

Com `hidden: true`, um livro não aparece na página nem em “Quem mais mora
aqui”, mas continua no `shelf.yaml` e nas versões. Tirar a marca e rodar
`draw` o devolve. O painel e `check` explicam quantos livros estão visíveis e
escondidos, sem custo.

## Boundary

A story foi aberta, não planejada. Não iniciar implementação até o Navigator
aprovar um plano.
