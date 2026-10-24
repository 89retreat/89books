---
status: Open
raised: 2026-10-24
decided:
deciders:
  - Navigator (Alisson)
supersedes:
related:
  - AGENTS.md
  - docs/process/development-guide.md
---

# Quem é o Navigator quando um colaborador trabalha

## Question

Pessoas que não usam o Mirror vão colaborar com os próprios agentes. Cada
colaborador é o Navigator da sua story (aprova o plano e valida), ou o Alisson
continua aprovando planos e validações, por exemplo via review de PR?

Importa porque define o que o agente faz em cada checkpoint e quem pode fazer
merge.

## Decision

Pending. Padrão provisório (Ariad): quem conduz a sessão é o Navigator dela, e
nada entra na branch principal sem review de outra pessoa do grupo.

## Rationale

## Options Considered

- Cada colaborador é Navigator da própria story; review de PR por outra pessoa.
- Alisson é Navigator de tudo; o colaborador conduz o Driver e pede aprovação
  nos checkpoints de plano e validação.
- Por tipo: Technical Stories com o colaborador; User Stories (experiência de
  leitura) com aprovação do Alisson.

## Consequences

Atualizar `AGENTS.md` e `docs/process/development-guide.md` (Driver and
Navigator, Branch/PR habits).

## Review Trigger

Primeiro colaborador entrando no projeto.
