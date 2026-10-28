---
status: Decided
raised: 2026-10-24
decided: 2026-10-26
deciders:
  - Navigator (Alisson)
  - grupo do dogfood
supersedes:
related:
  - CV4.DS1
  - CV4.DS2
  - ../../exploration/es-002-a-estante-num-arquivo/index.md
---

# Qual grupo do Telegram recebe os movimentos

## Question

Os movimentos vão para o grupo que os amigos já usam ou para um grupo criado só
para isso? Quem administra o bot?

## Decision

**Um grupo dedicado**, criado para o 89 Livros, com o bot como membro. O bot
publica ali só o que a pessoa escolhe compartilhar; as respostas são conversa
entre as pessoas e o bot não participa. Quem administra o bot e o grupo se
define ao planejar a CV4.

## Rationale

A amizade do grupo vive num grupo de WhatsApp, não no Telegram
([ES-002](../../exploration/es-002-a-estante-num-arquivo/index.md)). O
Telegram é ferramenta, não lugar social; um grupo novo protege o grupo de
amizade e deixa observar se os movimentos geram conversa.

## Options Considered

- **Grupo dedicado no Telegram** (escolhida).
- **Mensagens individuais do bot a cada membro**: viram notificação e perdem
  a conversa coletiva.
- **Levar os movimentos ao WhatsApp do grupo**: acerta o lugar, mas tem custo
  técnico e de plataforma não verificado; fora por enquanto.

## Consequences

- O bot vive em dois lugares: a conversa privada com cada pessoa e o grupo
  dedicado.
- Apresentar a estante ao grupo é um gesto da pessoa (CV4.DS1.US2).

## Review Trigger

Retrospectiva da CV4, ou o grupo pedindo os movimentos no WhatsApp.
