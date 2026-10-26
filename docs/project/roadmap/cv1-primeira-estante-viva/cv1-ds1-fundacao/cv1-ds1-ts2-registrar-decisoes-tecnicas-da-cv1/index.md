---
code: CV1.DS1.TS2
level: Technical Story
status: Active
status_reason: decisões reescritas para o MVP local pela ES-002; aguarda validação do Navigator
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
I want to fechar as decisões técnicas em aberto com o resultado do spike e da ES-002,
So that a DS2 e a DS3 partam de premissas registradas.

## Outcome

Os registros de decisão da CV1 que dependem de técnica ficam `Decided`, e o
briefing e o guia local ganham as premissas resultantes.

## Acceptance Behavior

```text
Given o relatório do spike TS1 e a ES-002
When o Navigator lê os registros de interface principal, acesso e compartilhamento, e stack
Then os três estão Decided para o MVP local, com opções consideradas e consequências
And a forma explorada para o Telegram fica registrada para a CV2
And o briefing (Architecture Premises) e o guia local refletem as decisões
```

## Scope

- Interface: script local que gera um HTML (CV1); bot do Telegram (CV2).
- Acesso e compartilhamento: arquivo ou GitHub Pages, à escolha da pessoa.
- Stack do script e custo por estante.
- Atualização de `briefing.md` e `development-guide.md`.

## Out Of Scope

- Onde publicar no GitHub Pages: fica como decisão aberta para a CV1.DS3.
- Navigator dos colaboradores: decisão de processo, independe desta story.
- Qualquer código.

## Revision

A primeira versão desta story (2026-10-26) propôs web app + bot, acesso por
link do bot e Django no Fly.io. Antes do aceite, a
[ES-002](../../../../exploration/es-002-a-estante-num-arquivo/index.md)
trocou o MVP por um script local, e as decisões foram reescritas. A forma com
servidor ficou registrada para a CV2.

## Validation

Navigator: os registros estão Decided com a justificativa reconhecida por ele.
