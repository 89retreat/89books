---
code: CV2.DS3.US4
level: User Story
status: Done
status_reason: validada por captura do Navigator, revisada sem dívida relevante e fechada em 2026-10-29
updated: 2026-10-29
related:
  - ../index.md
  - ../cv2-ds3-us1-put-each-book-on-the-shelf-i-choose/index.md
  - ../cv2-ds3-us3-choose-the-photo-that-represents-my-shelf/index.md
---

[< CV2.DS3](../index.md)

# CV2.DS3.US4 — Write my own shelf titles and texts

**Status:** Done

## User Story

Como pessoa que apresenta sua estante, quero escrever a abertura, os títulos e
os textos das minhas prateleiras para que a página fale com minhas palavras,
não apenas com o primeiro retrato proposto pela IA.

## Candidate Outcome

- `lens` no `shelf.yaml` controla literalmente a abertura da página.
- `title` e `text` de cada seção controlam literalmente o cabeçalho e o texto
  daquela prateleira, preservando ordem e livros.
- `*título*` continua marcando itálico sem permitir HTML arbitrário.
- Edições autorais sobrevivem a `check`, `draw`, histórico e restore; nenhuma
  operação gratuita chama modelo ou catálogo.
- Operações puras preparam os mesmos controles para uma interface futura.

## Plan

[plan.md](plan.md)

## Test Guide

[test-guide.md](test-guide.md)

## Next Checkpoint

Aprovação explícita do plano pelo Navigator. Implementação permanece bloqueada
até esse aceite.
