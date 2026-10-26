---
code: CV1.DS1
level: Delivery Story
status: Active
status_reason: puxada pelo Navigator; expandida em TS1, TS2 e TS3
updated: 2026-10-25
---

[< CV1](../index.md)

# CV1.DS1 — Fundação: reconhecimento de livros e decisões técnicas

**Status:** Active

---

## Outcome

Sabemos se uma foto de estante (e um print do Kindle) vira uma lista confiável
de livros, e as decisões técnicas da CV1 estão registradas, de modo que DS2 a
DS4 possam ser construídas sem retrabalho de base.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| [CV1.DS1.TS1](cv1-ds1-ts1-spike-da-foto-da-estante-a-lista-de-livros/index.md) | Spike: da foto da estante à lista de livros | Technical Story | Com fotos reais das estantes do grupo e um print do Kindle, medir quantos livros visíveis são reconhecidos e normalizados na Open Library (título, autor, capa), com custo e tempo por foto. O resultado decide a abordagem da DS2. | Done |
| [CV1.DS1.TS2](cv1-ds1-ts2-registrar-decisoes-tecnicas-da-cv1/index.md) | Registrar decisões técnicas da CV1 | Technical Story | Stack, hospedagem, modelo de acesso e forma do bot decididos nos registros abertos de `docs/project/decisions/records/` (interface, acesso, grupo do Telegram). | Active |
| [CV1.DS1.TS3](cv1-ds1-ts3-esqueleto-implantado/index.md) | Esqueleto implantado | Technical Story | App mínimo no ar, com acesso do grupo por convite e modelo de dados base: leitor, foto de estante, livro na estante (com a origem: foto, Kindle ou manual), movimento. | Planned |

## Done Condition

O spike tem resultado documentado, as decisões estão registradas e o esqueleto
está acessível pelos membros do grupo.
