---
code: CV2.DS1
level: Delivery Story
status: Planned
status_reason: criada na reorganização de 2026-10-27 com a antiga CV1.DS2.US4 e a CV1.DS2.TS1
updated: 2026-10-27
related:
  - ../../cv1-primeira-estante-viva/cv1-ds2-a-estante-num-arquivo/index.md
---

[< CV2](../index.md)

# CV2.DS1 — Corrigir a estante

**Status:** Planned

---

## Outcome

A pessoa corrige a estante sem pagar de novo pelo reconhecimento e pede outro
retrato quando não se reconhece.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| CV2.DS1.US1 | Corrigir a estante e pedir outro retrato | User Story | Apago ou corrijo livros no `books.yaml` e gero de novo em segundos, sem reconhecer as fotos outra vez; peço um retrato novo quando não me reconheço. Antes CV1.DS2.US4. | Planned |
| CV2.DS1.TS1 | Ler as fotos em faixas melhora o reconhecimento? | Technical Story | Medição com o gabarito da estante do Lula e o `recomparar.py`: foto inteira contra foto em faixas, em acerto, livros duplicados na emenda e custo. Gatilho: as estantes dos fundadores mostrarem erros de leitura demais para corrigir à mão. Antes CV1.DS2.TS1. | Planned |

## Done Condition

Cada fundador corrigiu a própria estante e a gerou de novo sem novo
reconhecimento.
