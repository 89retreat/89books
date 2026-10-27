---
code: CV3
level: Value
status: Planned
status_reason: depende da retrospectiva da CV1
updated: 2026-10-26
related:
  - ../../exploration/es-002-a-estante-num-arquivo/index.md
---

[< Roadmap](../index.md)

# CV3 — A Estante no Telegram

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

## Delivery Arc

| Code | Delivery Story | Outcome |
|------|----------------|---------|
| [CV3.DS1](cv3-ds1-o-bot-como-porta/index.md) | O bot como porta | A pessoa manda fotos ao bot e recebe o link da estante; apresenta a estante ao grupo dedicado quando quiser |
| [CV3.DS2](cv3-ds2-movimentos-que-circulam/index.md) | Movimentos que circulam | "Comecei a ler" e insights chegam ao grupo dedicado com link para a estante |

## Scope

Depende do que a retrospectiva da CV1 mostrar. Exige servidor: a direção
técnica explorada na TS2 da CV1 (Django + HTMX, SQLite, Fly.io) está
registrada em
[stack e hospedagem](../../decisions/records/2026-10-26T1332Z-stack-e-hospedagem.md)
e deve ser revista ao planejar esta CV.

Fora: levar os movimentos a grupos sociais já instituídos (o WhatsApp do
grupo), Mini Apps do Telegram.

## Acceptance / Done Condition

A definir quando a CV3 for puxada.
