---
code: CV4
level: Value
status: Planned
status_reason: era CV3 até 2026-10-28; a porta (bot ou aplicação web) está em decisão aberta
updated: 2026-10-28
related:
  - ../../exploration/es-002-a-estante-num-arquivo/index.md
---

[< Roadmap](../index.md)

# CV4 — A Estante no Telegram

**Status:** Planned

---

## Intent

O Telegram vira a porta da estante. A pessoa manda as fotos ao bot e recebe a
estante pronta, sem instalar nada nem configurar chave. A estante ganha vida
com dois movimentos, **comecei a ler** e **insight**, que o bot leva a um
grupo dedicado quando a pessoa escolhe compartilhar.

O desenho veio da
[ES-002](../../exploration/es-002-a-estante-num-arquivo/index.md):

- o bot vive em dois lugares: a conversa privada com cada pessoa (entrada,
  estante pronta, retrato, insights, comecei a ler) e um grupo dedicado, onde
  publica só o que a pessoa escolhe;
- apresentar a estante ao grupo é um gesto da pessoa e pode ser o seu primeiro
  movimento;
- o Telegram é requisito para o grupo e para futuros usuários;
- a estante abre também no navegador comum.

Pergunta: **movimentos simples, num grupo dedicado, fazem conversas nascerem
em torno das estantes?**

Esta é a CV que leva a estante a quem não usa o terminal. Em 2026-10-28 ficou
em aberto se a porta de entrada é o bot do Telegram ou uma aplicação web
([a porta para quem não usa o terminal](../../decisions/records/2026-10-28T1400Z-a-porta-para-quem-nao-usa-o-terminal.md)).
A CV4.DS1 pode mudar de forma com essa decisão; os movimentos no grupo do
Telegram (CV4.DS2) seguem a
[decisão do grupo](../../decisions/records/2026-10-24T2013Z-grupo-do-telegram.md).
O servidor roda o mesmo núcleo da estante que o terminal usa desde a CV2
([terminal como cliente fino](../../decisions/records/2026-10-28T1400Z-terminal-como-cliente-fino.md)).

## Delivery Arc

| Code | Delivery Story | Outcome |
|------|----------------|---------|
| [CV4.DS1](cv4-ds1-o-bot-como-porta/index.md) | O bot como porta | A pessoa manda fotos ao bot e recebe o link da estante; apresenta a estante ao grupo dedicado quando quiser |
| [CV4.DS2](cv4-ds2-movimentos-que-circulam/index.md) | Movimentos que circulam | "Comecei a ler" e insights chegam ao grupo dedicado com link para a estante |

## Scope

Depende do que a retrospectiva da CV2 mostrar sobre as edições que as
pessoas fazem. Exige servidor: a direção
técnica explorada na TS2 da CV1 (Django + HTMX, SQLite, Fly.io) está
registrada em
[stack e hospedagem](../../decisions/records/2026-10-26T1332Z-stack-e-hospedagem.md)
e deve ser revista ao planejar esta CV.

Fora: levar os movimentos a grupos sociais já instituídos (o WhatsApp do
grupo), Mini Apps do Telegram.

## Acceptance / Done Condition

A definir quando a CV4 for puxada.
