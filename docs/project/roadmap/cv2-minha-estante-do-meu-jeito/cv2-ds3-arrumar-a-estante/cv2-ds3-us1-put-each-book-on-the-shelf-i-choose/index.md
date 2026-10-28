---
code: CV2.DS3.US1
level: User Story
status: Active
status_reason: puxada pelo Navigator em 2026-10-28 depois da conclusão de CV2.DS2.US2; aguarda plano
updated: 2026-10-28
related:
  - ../index.md
  - ../../cv2-ds2-corrigir-a-estante/cv2-ds2-us2-fix-titles-authors-and-covers/index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/cv2-ds1-ts2-shelf-yaml-v1/index.md
---

[< Parent](../index.md)

# CV2.DS3.US1 — Put each book on the shelf I choose

**Status:** Active
**Type:** User Story

---

## User Story

In order to revelar a minha própria lógica de organização,
As uma pessoa que quer arrumar a estante gerada,
I want mover livros entre prateleiras e escolher sua ordem no `shelf.yaml`,
So that a página mostre cada livro no lugar que eu escolhi.

## Outcome

Mover a entrada completa de um livro entre listas `books` muda a prateleira e
a posição dele na página após um `draw` gratuito. Reordenar, criar ou remover
prateleiras no arquivo também muda a página, sem catálogo, modelo ou perda de
metadados do livro.

## Boundary

A story foi puxada e preparada, mas ainda não tem plano aprovado. Não iniciar
implementação. O plano deve caracterizar o comportamento já existente antes
de decidir o mínimo que falta e incluir uma operação pura de movimento para
uma futura interface.
