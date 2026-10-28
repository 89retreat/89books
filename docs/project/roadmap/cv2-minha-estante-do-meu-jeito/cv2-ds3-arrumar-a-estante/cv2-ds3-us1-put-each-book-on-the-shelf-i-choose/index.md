---
code: CV2.DS3.US1
level: User Story
status: Done
status_reason: validada e fechada pelo Navigator em 2026-10-28; 191 testes e E2E gratuito aprovados
updated: 2026-10-28
related:
  - ../index.md
  - ../../cv2-ds2-corrigir-a-estante/cv2-ds2-us2-fix-titles-authors-and-covers/index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/cv2-ds1-ts2-shelf-yaml-v1/index.md
---

[< Parent](../index.md)

# CV2.DS3.US1 — Put each book on the shelf I choose

**Status:** Done
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
metadados do livro. Uma prateleira criada pela pessoa continua regular mesmo
quando é a última e não tem texto; só a seção intitulada “E mais livros que já
me acompanharam” conserva o tratamento visual de fechamento.

## Acceptance Behavior

```text
Given a book with reader and catalogue metadata in one shelf
When I move its complete YAML entry to another shelf and run check then draw
Then it appears in the chosen shelf and exact chosen position
And all of its fields are preserved without network, key or cost
```

```text
Given ordered shelf sections in shelf.yaml
When I reorder, add or remove an empty section and redraw
Then the page follows the authored section order
And a custom last section without text is not mistaken for the generated closing shelf
```

```text
Given a future UI calling the reusable core
When it moves a book, reorders a shelf, adds a shelf or removes an empty shelf
Then it receives a new ShelfFile without mutating the original
And removing a non-empty shelf is rejected rather than deleting books implicitly
```

## Scope

- Caracterizar a ordem literal de prateleiras e livros já existente no renderer.
- Corrigir a detecção da prateleira final para depender também do título canônico.
- Operações puras para mover livro, adicionar, reordenar e remover prateleira vazia.
- Exemplos de edição do bloco YAML completo e redraw gratuito.
- Validação numa cópia descartável, sem comparar histórico real.

## Out Of Scope

- Interface drag-and-drop ou novo comando de terminal.
- Excluir livros junto com uma prateleira.
- Escolher frente/lombada, foto em destaque, títulos ou textos; são stories seguintes.
- Agrupar automaticamente por autor ou reescrever a organização da pessoa.
- Alterar o formato `shelf.yaml` v1.

## Validation

Gratuita: numa cópia descartável, mover um livro completo para uma nova
prateleira, reordenar as seções, desenhar e abrir; depois esvaziar e remover a
prateleira criada. A página deve seguir o arquivo e o histórico deve registrar
cada fonte desenhada, sem chave, catálogo ou modelo.
