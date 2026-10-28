---
code: CV2.DS2.US1
level: User Story
status: Validated
status_reason: Navigator escondeu e trouxe de volta um livro numa estante real descartável; debt review sem nova dívida aguarda confirmação
updated: 2026-10-28
related:
  - ../index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/cv2-ds1-us3-never-lose-an-edit/index.md
---

[< Parent](../index.md)

# CV2.DS2.US1 — Hide books from my shelf

**Status:** Validated
**Type:** User Story

---

## User Story

In order to a estante mostrar apenas o que quero mostrar,
As uma pessoa que revisa a própria estante,
I want esconder um livro sem apagá-lo do meu arquivo,
So that posso trazê-lo de volta quando quiser e preservar meu histórico.

## Outcome

Com `hidden: true`, um livro não aparece como capa ou lombada na página nem
participa de “Quem mais mora aqui”, mas continua no `shelf.yaml` e nas versões.
Tirar a marca e rodar `draw` o devolve no mesmo lugar. O painel e `check`
explicam quantos livros estão visíveis e escondidos, sem custo.

O texto já escrito da lente ou da prateleira não é reescrito automaticamente;
se ele citar o título escondido, a pessoa continua podendo editá-lo diretamente.

## Acceptance Behavior

```text
Given a visible book in shelf.yaml
When I add `hidden: true` and run `check` then `draw`
Then the book has no cover or spine in shelf.html
And total, visible and hidden counts remain understandable
And the changed source is preserved by history
```

```text
Given a hidden book whose author would otherwise appear in “Quem mais mora aqui”
When the page is drawn
Then that book does not contribute to the author frequency
```

```text
Given a hidden book
When I remove `hidden: true` and draw again
Then the book returns to its original shelf position
And no paid service, key or network call is used
```

## Scope

- Contract tests for hidden, visible and explicitly `hidden: false` books.
- Filtering before shelf layout and frequent-author aggregation.
- Pure named operations for a future server/UI to hide and show a selected
  book without choosing folders or writing files.
- Status/check/draw/history integration and user documentation.

## Out Of Scope

- Deleting books from `shelf.yaml`.
- Rewriting lens or shelf prose that mentions a hidden title.
- Moving the book, changing its title/author/cover or adding a terminal
  `hide` command.
- Comparing real history versions without explicit consent.

## Validation

Free validation on a disposable copy: hide one chosen book, draw/open it,
confirm counts, remove the mark, draw/open again and confirm its return.
