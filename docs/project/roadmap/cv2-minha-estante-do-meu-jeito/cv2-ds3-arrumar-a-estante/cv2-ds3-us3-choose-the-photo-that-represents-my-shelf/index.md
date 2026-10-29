---
code: CV2.DS3.US3
level: User Story
status: Validated
status_reason: validação aceita pelo Navigator em 2026-10-29; aguarda debt review e fechamento
updated: 2026-10-29
related:
  - ../index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/cv2-ds1-us1-create-once-draw-for-free/index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/cv2-ds1-us2-know-where-my-shelf-stands/index.md
---

[< CV2.DS3](../index.md)

# CV2.DS3.US3 — Choose the photo that represents my shelf

**Status:** Validated

## User Story

Como pessoa que mostra sua estante, quero escolher em `cover_photo` qual das
minhas fotos abre o mosaico para que a presença física que representa a
estante seja uma decisão minha, não uma ordem de arquivo nem uma configuração
antiga.

## Outcome

- `cover_photo` escolhe uma foto existente na pasta da estante pelo nome exato.
- A foto escolhida aparece primeiro e recebe o espaço de destaque do mosaico.
- As demais fotos conservam sua ordem determinística.
- `check` e `draw` recusam a mesma escolha ausente sem substituir a página nem
  criar histórico.
- Depois que existe `shelf.yaml`, `config.toml` não decide mais a foto; uma
  marca antiga só participa da criação inicial e a escolha atual sobrevive a
  `recreate` quando o arquivo ainda existe.
- Uma operação pura prepara a mesma escolha para uma interface futura.

## Acceptance Behavior

```text
Given uma estante com várias fotos e cover_photo apontando para uma delas
When eu confiro e redesenho gratuitamente
Then essa foto abre o mosaico em destaque e as demais mantêm sua ordem
And config.toml, rede, modelos e catálogos não participam da decisão

Given cover_photo apontando para um arquivo ausente ou fora das fotos da estante
When eu rodo check ou draw
Then recebo um erro claro com o nome escolhido
And shelf.html, marcador e histórico existentes permanecem intactos
```

## Plan

[plan.md](plan.md)

## Test Guide

[test-guide.md](test-guide.md)
