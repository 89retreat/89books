# Product Design Proposal: A Primeira Estante Viva

## Product Intent

Construir um experimento mínimo para um pequeno grupo de leitores. Cada pessoa oferece uma foto de uma estante, um print do Kindle ou um conjunto inicial de livros. O sistema reconhece os títulos, cria uma estante virtual visitável e usa a imagem física como capa ou miniatura quando disponível. A experiência ganha vida por movimentos simples: começar a ler um livro e registrar insights durante a leitura. Esses movimentos são enviados a um grupo compartilhado no Telegram, onde as conversas já podem acontecer. O objetivo é descobrir se estantes visíveis e sinais de leitura geram curiosidade, visitas, perguntas e circulação entre pessoas.

## User-Facing Behavior

A Estante como Retrato e Campo de Ressonância

## What The Product Should Feel Like

The product should preserve the exploratory shape discovered by Explorer Mode. It should show the user what is happening at the product level, not expose implementation mechanics first.

## Interaction Flow

- User works in Explorer Mode while uncertainty is still alive.
- Explorer surfaces story changes visibly.
- Explorer names attractors and proposes small experiments.
- Explorer proposes Builder handoff only when the user asks or confirms readiness.
- Builder begins only after explicit confirmation.

## Product-Level States

- Exploratory Story active.
- Attractor proposed or accepted.
- Experiment proposal proposed or accepted.
- Builder handoff proposed.

## Acceptance Behavior

- The user can understand what is being proposed without reading implementation details.
- The proposal preserves uncertainty and open questions.
- The proposal gives Builder enough product shape to create roadmap or story plans.

## Explicit Non-Goals

- This document does not define implementation architecture.
- This document does not create delivery tasks by itself.
- This document does not replace Builder planning.

## Open Product Questions

- Which behavior is necessary for the first delivery slice?
- What should remain exploratory after Builder starts?
- What user validation will prove the product behavior works?
