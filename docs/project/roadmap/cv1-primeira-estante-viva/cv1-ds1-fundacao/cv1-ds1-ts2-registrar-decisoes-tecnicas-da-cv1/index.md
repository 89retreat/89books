---
code: CV1.DS1.TS2
level: Technical Story
status: Active
status_reason: decisões registradas; aguarda validação do Navigator
updated: 2026-10-26
related:
  - ../../../../decisions/records/
---

[< Parent](../index.md)

# CV1.DS1.TS2 — Registrar decisões técnicas da CV1

**Status:** Active
**Type:** Technical Story

---

## Technical Story

In order to construir a CV1 sem retrabalho de base,
As o time do projeto,
I want to fechar as decisões técnicas em aberto com o resultado do spike,
So that a TS3 e as DS2 a DS4 partam de premissas registradas.

## Outcome

Os registros de decisão da CV1 que dependem de técnica passam de `Open` para
`Decided`, e o guia local ganha os comandos e premissas resultantes.

## Acceptance Behavior

```text
Given o relatório do spike TS1
When o Navigator decide interface principal, acesso do grupo e stack/hospedagem
Then os registros "interface principal" e "acesso do grupo" ficam Decided, com opções consideradas e consequências
And a stack e a hospedagem ficam registradas num novo registro de decisão
And o briefing (Architecture Premises) e o guia local refletem as decisões
```

## Scope

- Interface principal: web app, bot do Telegram ou híbrido.
- Acesso do grupo: links por convite ou login pelo Telegram.
- Stack, hospedagem e custo mensal esperado.
- Atualização de `briefing.md` e `development-guide.md`.

## Out Of Scope

- Grupo do Telegram e privacidade dos insights: ficam para a DS4.
- Navigator dos colaboradores: decisão de processo, independe desta story.
- Qualquer código.

## Validation

Navigator: os registros estão Decided com a justificativa reconhecida por ele.
