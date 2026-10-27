---
code: CV1.DS2
level: Delivery Story
status: Done
status_reason: US1, US2 e US3 concluídas; correção e medição em faixas movidas para a CV2.DS1 em 2026-10-27
updated: 2026-10-27
related:
  - ../../../exploration/es-002-a-estante-num-arquivo/index.md
---

[< CV1](../index.md)

# CV1.DS2 — A estante num arquivo

**Status:** Done

---

## Outcome

Uma pessoa do grupo põe fotos da estante ou das prateleiras numa pasta,
configura a chave do OpenRouter e roda um script. Recebe um HTML autocontido
e bonito da sua estante, com as fotos, os livros e o retrato de si. A estante
aparece na hora com a leitura da IA e é corrigida aos poucos, sem formulário.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| [CV1.DS2.US1](cv1-ds2-us1-gerar-minha-estante/index.md) | Gerar minha estante a partir de uma pasta de fotos | User Story | Rodo o script numa pasta de fotos e recebo um HTML autocontido, com as fotos embutidas, os livros reconhecidos e o retrato (lente e temas que se repetem). | Done |
| [CV1.DS2.US2](cv1-ds2-us2-uma-estante-bonita/index.md) | Uma estante bonita, mesmo sem capas | User Story | A página abre com um mosaico das fotos e a lente em primeira pessoa; os livros aparecem em prateleiras desenhadas, uma por situação de leitura, como lombadas, com os livros citados de frente. | Done |
| [CV1.DS2.US3](cv1-ds2-us3-livros-certos-na-estante/index.md) | Os livros certos, com quem os escreveu | User Story | A estante confere sozinha título e autoria (modelo e Google Books), mostra o autor nas lombadas e apresenta as sobras como mais livros que já me acompanharam, com os autores em primeiro plano nas lombadas. | Done |

## Done Condition

O comando gera, a partir de uma pasta de fotos, uma estante bonita com o
retrato de si, títulos e autores conferidos. Cumprida em 2026-10-27 sobre a
estante do Lula.

A correção pelo `books.yaml`, o novo retrato e a medição da leitura em faixas
(antes US4 e TS1) foram para a
[CV2.DS1](../../cv2-a-estante-visitavel/cv2-ds1-corrigir-a-estante/index.md)
na reorganização de 2026-10-27, que fechou a CV1 em torno da capacidade de ir
do clone à estante.
