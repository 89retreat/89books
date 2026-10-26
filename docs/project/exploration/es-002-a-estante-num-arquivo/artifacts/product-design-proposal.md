# Product Design Proposal: A Estante num Arquivo

## Product Intent

Reorganizar a CV1 em torno de um MVP local: cada pessoa põe as fotos da estante ou das prateleiras numa pasta, configura a chave do OpenRouter num arquivo e roda um script Python. O resultado é um HTML autocontido e bonito da sua estante, com as fotos, a capa escolhida, os livros (com visual próprio para os ~40% sem capa na Open Library) e o retrato de si em duas partes, a lente e os temas que se repetem. A pessoa corrige apagando linhas de um arquivo de livros e rodando de novo, com o reconhecimento em cache, e pode gerar o retrato outra vez. Ela escolhe compartilhar o arquivo, publicar no GitHub Pages ou as duas coisas. Sem bot, servidor, login ou hospedagem. O Telegram (bot como porta, grupo dedicado, movimentos) passa para uma CV seguinte, já com as respostas desta exploração.

## User-Facing Behavior

O Telegram como Porta da Estante

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
