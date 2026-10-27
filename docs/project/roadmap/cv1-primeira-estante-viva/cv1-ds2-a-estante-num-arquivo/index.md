---
code: CV1.DS2
level: Delivery Story
status: Active
status_reason: US1 e US2 concluídas; US3 em andamento
updated: 2026-10-26
related:
  - ../../../exploration/es-002-a-estante-num-arquivo/index.md
---

[< CV1](../index.md)

# CV1.DS2 — A estante num arquivo

**Status:** Active

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
| [CV1.DS2.US3](cv1-ds2-us3-livros-certos-na-estante/index.md) | Os livros certos, com quem os escreveu | User Story | A estante confere sozinha título e autoria (modelo e Google Books), mostra o autor nas lombadas e apresenta as sobras como livros que um dia me chamaram a atenção. | Active |
| CV1.DS2.TS1 | Ler as fotos em faixas melhora o reconhecimento? | Technical Story | Medição com o gabarito da estante do Lula e o `recomparar.py`: foto inteira contra foto em faixas, em acerto, livros duplicados na emenda e custo. Gatilho: as estantes dos fundadores mostrarem erros de leitura demais para corrigir à mão no `books.yaml`. | Planned |
| CV1.DS2.US4 | Corrigir a estante e pedir outro retrato | User Story | Apago ou corrijo livros no arquivo de livros e rodo de novo em segundos, sem reconhecer as fotos outra vez; peço um retrato novo quando não me reconheço. | Planned |

## Done Condition

Cada pessoa do grupo gerou a própria estante, corrigiu o que quis e tem um
HTML que abre bem no celular e no computador.
