---
code: CV2.DS2.US2
level: User Story
status: Active
status_reason: puxada em 2026-10-28; aguarda preparação e plano aprovado pelo Navigator
updated: 2026-10-28
related:
  - ../index.md
  - ../cv2-ds2-us1-hide-books-from-my-shelf/index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/cv2-ds1-us3-never-lose-an-edit/index.md
---

[< Parent](../index.md)

# CV2.DS2.US2 — Fix titles, authors and covers

**Status:** Active
**Type:** User Story

---

## User Story

In order to a estante dizer os livros como eu os reconheço,
As uma pessoa que vê um título, autor ou capa errados,
I want corrigir esses dados diretamente no `shelf.yaml`,
So that a página mostre a minha estante, sem uma nova leitura paga das fotos.

## Outcome

A pessoa corrige `title`, `authors` e `known_as`, ou escolhe `cover` como imagem
na pasta, URL ou `none`; `draw` mostra a correção gratuitamente. Imagens locais
muito grandes são recusadas com um aviso claro. A fonte e o histórico preservam
a edição.

## Boundary

A story foi aberta, não planejada. Não iniciar implementação até o Navigator
aprovar um plano.
