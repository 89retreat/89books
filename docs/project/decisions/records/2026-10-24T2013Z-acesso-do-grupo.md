---
status: Decided
raised: 2026-10-24
decided: 2026-10-26
deciders:
  - Navigator (Alisson), por delegação ao Driver em cadência accelerated; aceite na validação da CV1.DS1.TS2
supersedes:
related:
  - CV1.DS1.TS3
---

# Como o grupo acessa o produto

## Question

O acesso fechado do grupo usa links mágicos por e-mail, identidade do Telegram
ou outro mecanismo?

## Decision

**Link de acesso enviado pelo bot do Telegram.** A pessoa abre o bot do 89
Livros e toca em "Entrar". O bot responde com um link pessoal de uso único,
válido por 15 minutos, que abre uma sessão de 90 dias no navegador.

Só entra quem está na **lista de membros**, pelo ID do Telegram, mantida por
quem administra o app. Quem abre um link de estante sem sessão vê uma página
que aponta para o bot.

## Rationale

- Todos do grupo já têm Telegram. Não há senha, e-mail nem cadastro.
- O bot já é necessário para os movimentos, então o acesso não acrescenta
  infraestrutura.
- O ID do Telegram identifica a pessoa e liga os movimentos ao autor sem um
  segundo mapeamento.
- A lista explícita separa o acesso da escolha do grupo que recebe os
  movimentos, que segue em aberto
  ([grupo do Telegram](2026-10-24T2013Z-grupo-do-telegram.md)).

## Options Considered

- **Link pelo bot com lista de membros** (escolhida).
- **Link mágico por e-mail**: exige serviço de envio e uma identidade a mais.
- **Widget de login do Telegram na página**: exige configurar o domínio no
  BotFather e confirmar pelo número de telefone, mais atrito no celular.
- **Entra quem está no grupo do Telegram** (consulta ao grupo): elegante, mas
  amarra o acesso a uma decisão ainda aberta. Pode substituir a lista depois.

## Consequences

- A TS3 cria o bot (BotFather), guarda o token como segredo e implementa o
  fluxo `/start` → link → sessão.
- A lista de membros é uma tabela administrável; adicionar alguém não exige
  deploy.
- Links compartilhados no grupo levam à estante depois do acesso.

## Review Trigger

Abertura para pessoas fora do grupo, ou decisão de usar a participação no
grupo do Telegram como critério de acesso.
