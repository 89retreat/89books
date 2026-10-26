---
status: Decided
raised: 2026-10-24
decided: 2026-10-26
deciders:
  - Navigator (Alisson), por delegação ao Driver em cadência accelerated; aceite na validação da CV1.DS1.TS2
supersedes:
related:
  - CV1.DS1.TS2
---

# Interface principal da CV1

## Question

A entrada e os movimentos acontecem num web app pensado para celular, ou o bot
do Telegram é a interface principal (recebe foto, comandos e insights), com a
estante visitável como página web?

Importa porque define a stack, o esforço da DS2 e da DS4 e o quanto o grupo
precisa instalar ou aprender.

## Decision

**Híbrido.** Um web app pensado para celular é a interface principal: entrada,
revisão do reconhecimento, estante, visita e registro dos movimentos. O bot do
Telegram só **envia**: os movimentos para o grupo (DS4) e o link de acesso para
cada pessoa (ver [acesso do grupo](2026-10-24T2013Z-acesso-do-grupo.md)).

## Rationale

- A revisão é obrigatória
  ([reconhecimento de livros](2026-10-24T2013Z-reconhecimento-de-livros.md)) e
  envolve dezenas de livros por foto (até ~20 por prateleira no spike):
  remover, corrigir e buscar num chat seria um formulário pior que o vazio.
- "A estante é o centro" pede capas reunidas e a foto da estante como capa.
  Isso só existe numa página.
- O Telegram continua sendo onde a conversa acontece; o produto não precisa
  receber comandos por lá para isso.
- Um web app abre por link, sem instalação, como pede o briefing.

## Options Considered

- **Web app com bot só para enviar** (escolhida).
- **Bot como interface principal**, com páginas só para ver estantes: menos
  atrito para mandar a foto, mas revisão e movimentos ficariam presos ao
  formato de conversa.
- **Entrada pelo bot e revisão no web app**: duas portas para a mesma tarefa
  na CV1; fica como evolução se o grupo pedir.

## Consequences

- DS2 e DS3 são páginas web otimizadas para celular; a DS4 registra os
  movimentos na web e o bot publica no grupo.
- O bot existe desde a TS3, por causa do acesso.
- Mandar foto direto ao bot fica fora da CV1.

## Review Trigger

Se o grupo pedir para mandar fotos ou insights pelo Telegram durante o
dogfood, ou se a revisão no celular se mostrar penosa.
