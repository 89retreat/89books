---
status: Decided
raised: 2026-10-24
decided: 2026-10-26
deciders:
  - Navigator (Alisson), por delegação ao Driver em cadência accelerated; aceite na validação da CV1.DS1.TS2
supersedes:
related:
  - CV1.DS1.TS2
  - CV1.DS2
  - CV4.DS1
  - ../../exploration/es-002-a-estante-num-arquivo/index.md
---

# Interface principal da CV1

## Question

A entrada e os movimentos acontecem num web app pensado para celular, ou o bot
do Telegram é a interface principal (recebe foto, comandos e insights), com a
estante visitável como página web?

Importa porque define a stack, o esforço da DS2 e da DS4 e o quanto o grupo
precisa instalar ou aprender.

## Decision

**CV1: um script local.** A pessoa põe as fotos numa pasta, configura a chave
do OpenRouter e roda um script Python, que gera um HTML autocontido da sua
estante. Não há web app, bot nem servidor.

**CV4: o Telegram como porta.** A entrada e os movimentos passam para o bot
do Telegram; a estante continua sendo uma página, que abre também no
navegador comum. A forma está descrita na
[CV4](../../roadmap/cv4-a-estante-no-telegram/index.md).

## Rationale

- A [ES-002](../../exploration/es-002-a-estante-num-arquivo/index.md) partiu
  do prêmio que a pessoa recebe: uma estante bonita com um retrato de si. Bot,
  servidor e login existiam só para entregar esse prêmio; o script entrega o
  mesmo prêmio sem eles.
- Todos os colaboradores do dogfood são técnicos; rodar um script com `uv` não
  é atrito para eles.
- O experimento com o Lula mostrou que o retrato funciona; o que falta saber é
  se a estante dá vontade de ser mostrada, e isso não exige o bot.
- A revisão obrigatória, que pesava contra o bot, deixou de existir: a estante
  aparece na hora e é corrigida aos poucos
  ([reconhecimento de livros](2026-10-24T2013Z-reconhecimento-de-livros.md)).

## Options Considered

- **Script local que gera HTML** (escolhida para a CV1).
- **Bot como porta, estante como página** (escolhida para a CV4): menor
  atrito para quem não programa; exige servidor.
- **Web app com bot só para enviar**: proposta inicial da TS2; a revisão no
  web app perdeu o motivo quando a revisão obrigatória saiu.
- **Mini Apps do Telegram**: guardados como sinal para depois.
- **Levar os movimentos ao WhatsApp do grupo**: fora por enquanto.

## Consequences

- A CV1 se organiza em torno do script (CV1.DS2); o compartilhamento por
  link ficou na CV3.DS1. A CV1.DS1.TS3 (esqueleto implantado) foi descartada.
- O bot, o grupo dedicado e os movimentos vão para a CV4.
- O código do script deve ficar reaproveitável pelo servidor da CV4.

## Revisão de 2026-10-28

Os códigos seguem a renumeração de 2026-10-28 (o Telegram é a CV4). Duas
decisões novas desdobram esta: o código do script reaproveitável pelo
servidor virou regra em
[o terminal como cliente fino](2026-10-28T1400Z-terminal-como-cliente-fino.md),
e o Telegram como porta voltou a ser uma pergunta em
[a porta para quem não usa o terminal](2026-10-28T1400Z-a-porta-para-quem-nao-usa-o-terminal.md).

## Review Trigger

Retrospectiva da CV1, ou pessoas de fora do grupo técnico querendo a própria
estante.
