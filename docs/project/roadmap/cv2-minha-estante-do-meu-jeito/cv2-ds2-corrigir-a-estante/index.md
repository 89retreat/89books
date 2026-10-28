---
code: CV2.DS2
level: Delivery Story
status: Planned
status_reason: era CV2.DS1 até 2026-10-28; reescrita sobre o shelf.yaml; depende da CV2.DS1
updated: 2026-10-28
related:
  - ../index.md
  - ../cv2-ds1-a-estante-num-arquivo-meu/index.md
---

[< CV2](../index.md)

# CV2.DS2 — Corrigir a estante

**Status:** Planned

---

## Outcome

A pessoa conserta o que a leitura errou, editando o `shelf.yaml` e rodando
`draw`: esconde o que não é dela ou não quer mostrar e corrige títulos,
autores e capas. O livro escondido continua no arquivo, para voltar quando ela
quiser.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| CV2.DS2.US1 | Hide books from my shelf | User Story | Com `hidden: true`, um livro some da página e do "Quem mais mora aqui", mas fica no arquivo; tirar a marca o traz de volta. | Planned |
| CV2.DS2.US2 | Fix titles, authors and covers | User Story | Corrijo `title` e `authors` (inclusive o nome da lombada, `known_as`) e escolho a capa: uma imagem na pasta, um link, ou `cover: none` para mostrar a lombada; imagens grandes demais são recusadas com aviso. Resolve as capas que são páginas amareladas e as iniciais de catálogo nos nomes. | Planned |
| CV2.DS2.TS1 | Does reading photos in strips improve recognition? | Technical Story | Medição com o gabarito da estante do Lula e o `recomparar.py`: foto inteira contra foto em faixas, em acerto, duplicados na emenda e custo. Gatilho: as estantes dos fundadores mostrarem erros de leitura demais para corrigir à mão. Era CV2.DS1.TS1. | Planned |

## Done Condition

Um fundador escondeu e corrigiu livros na própria estante e a redesenhou, sem
perder as correções numa segunda rodada de `draw`.
