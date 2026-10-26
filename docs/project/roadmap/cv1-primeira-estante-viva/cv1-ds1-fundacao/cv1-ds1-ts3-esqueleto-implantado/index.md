---
code: CV1.DS1.TS3
level: Technical Story
status: Dropped
status_reason: ES-002 trocou o app no ar por um script local; a necessidade volta na CV2.DS1.TS1
updated: 2026-10-26
related:
---

[< Parent](../index.md)

# CV1.DS1.TS3 — Esqueleto implantado

**Status:** Dropped
**Type:** Technical Story

---

## Technical Story

In order to que as stories de produto (DS2 a DS4) só acrescentem comportamento,
As o time do projeto,
I want to colocar no ar um app mínimo na stack decidida, com acesso do grupo e o modelo de dados base,
So that cada story seguinte possa ser validada no celular por qualquer membro do grupo.

## Outcome

Um app mínimo publicado, acessível só aos membros do grupo, com testes e
deploy funcionando e o modelo de dados base criado.

## Acceptance Behavior

```text
Given as decisões da TS2 registradas
When um membro do grupo abre o endereço do app no celular e entra pelo acesso escolhido
Then ele vê uma página inicial do 89books identificada com seu nome
And quem não é do grupo não consegue entrar
And o repositório tem comandos de instalação, teste e execução no guia local
And o modelo de dados tem leitor, foto de estante, livro na estante (com origem: foto, Kindle ou manual, e ligação à obra da Open Library) e movimento
```

## Scope

- Projeto inicial na stack decidida, com testes e um pipeline de deploy.
- Acesso fechado ao grupo.
- Modelo de dados base, sem telas de produto.
- Comandos em `docs/process/development-guide.md`.

## Out Of Scope

- Upload de foto, reconhecimento e revisão (DS2).
- Página de estante (DS3).
- Movimentos e Telegram (DS4).

## Validation

Automatizada: testes passando e deploy concluído.
Navigator: entrar pelo celular com a própria conta e confirmar que alguém de
fora não entra.
