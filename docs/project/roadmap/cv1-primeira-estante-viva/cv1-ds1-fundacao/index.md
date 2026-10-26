---
code: CV1.DS1
level: Delivery Story
status: Active
status_reason: TS1 concluída; TS2 revista pela ES-002; TS3 descartada
updated: 2026-10-26
---

[< CV1](../index.md)

# CV1.DS1 — Fundação: reconhecimento de livros e decisões técnicas

**Status:** Active

---

## Outcome

Sabemos se uma foto de estante (e um print do Kindle) vira uma lista confiável
de livros, e as decisões técnicas do MVP local estão registradas, de modo que
a DS2 e a DS3 possam ser construídas sem retrabalho de base.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| [CV1.DS1.TS1](cv1-ds1-ts1-spike-da-foto-da-estante-a-lista-de-livros/index.md) | Spike: da foto da estante à lista de livros | Technical Story | Com fotos reais das estantes do grupo e um print do Kindle, medir quantos livros visíveis são reconhecidos e normalizados na Open Library (título, autor, capa), com custo e tempo por foto. O resultado decide a abordagem da DS2. | Done |
| [CV1.DS1.TS2](cv1-ds1-ts2-registrar-decisoes-tecnicas-da-cv1/index.md) | Registrar decisões técnicas da CV1 | Technical Story | Interface, compartilhamento e stack do MVP local decididos em `docs/project/decisions/records/`, revistos pela ES-002. | Active |
| [CV1.DS1.TS3](cv1-ds1-ts3-esqueleto-implantado/index.md) | Esqueleto implantado | Technical Story | App mínimo no ar com acesso do grupo. Descartada pela ES-002: o MVP local não tem servidor; a necessidade volta na CV2.DS1.TS1. | Dropped |

## Done Condition

O spike tem resultado documentado e as decisões técnicas do MVP local estão
registradas e aceitas pelo Navigator.
