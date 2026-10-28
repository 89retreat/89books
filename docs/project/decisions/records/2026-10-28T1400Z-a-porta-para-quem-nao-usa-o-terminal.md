---
status: Open
raised: 2026-10-28
decided:
deciders:
  - Navigator (Alisson)
  - grupo do dogfood
supersedes:
related:
  - CV4
  - CV4.DS1
  - 2026-10-24T2013Z-interface-principal.md
  - 2026-10-28T1400Z-terminal-como-cliente-fino.md
---

# A porta para quem não usa o terminal: bot do Telegram ou aplicação web

## Question

Quando o produto chegar a pessoas não técnicas, por onde elas entram: pelo
bot do Telegram (mandam as fotos numa conversa e recebem o link) ou por uma
aplicação web com cadastro e edição na tela?

Vêm junto duas perguntas que o terminal adia:

- **Quem paga** o reconhecimento e o retrato, quando não for a chave da
  própria pessoa: o grupo, um limite gratuito, uma cobrança?
- **As fotos num servidor nosso.** No terminal, as fotos não saem da máquina
  da pessoa. Com a porta, saem. O que prometemos, guardamos e apagamos?

## Decision

Pending

## Rationale

A [interface principal](2026-10-24T2013Z-interface-principal.md) escolheu o
Telegram como porta para depois da CV1, e a CV4 foi desenhada assim. Em
2026-10-28 o Navigator nomeou a aplicação web como alternativa. As edições da
CV2 (esconder, corrigir, arrumar) pesam a favor de uma tela; os movimentos no
grupo do Telegram pesam a favor do bot. Os dois podem conviver: o bot como
entrada e os movimentos, uma página web para editar.

Evidência que falta: quais edições os fundadores fizeram na CV2 e quanto, e o
que o primeiro amigo não técnico consegue fazer sozinho.

## Options Considered

- Bot do Telegram como porta, estante como página (a CV4 atual).
- Aplicação web com cadastro, envio de fotos e edição na tela.
- Bot para entrar e para os movimentos, página web para editar.

## Consequences

## Review Trigger

O primeiro amigo não técnico que queira a própria estante, ou a retrospectiva
da CV2.
