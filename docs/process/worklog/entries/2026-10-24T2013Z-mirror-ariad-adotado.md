---
date: 2026-10-24T20:13:17Z
author: Mirror Builder (Driver) com Alisson (Navigator)
kind: milestone
related:
  - ES-001
  - CV1
verification:
  - uv run python -m memory build pull-candidates --journey 89-livros --method ariad
---

# Projeto iniciado no Ariad, aberto a colaboradores sem Mirror

## What changed

A exploração ES-001 foi promovida para Delivery como CV1 A Primeira Estante
Viva, com quatro Delivery Stories e onze stories candidatas. O projeto adotou
o Ariad seguindo os modelos públicos de https://github.com/mirror-mind-ai/ariad:
`AGENTS.md`, guia local, briefing, princípios de produto, decisões, dívida
técnica, worklog e exploração, cada um no seu arquivo.

## Why it matters

Pessoas que não usam o Mirror Mind vão colaborar com os próprios agentes. Com o
`AGENTS.md` e o estado do projeto nos arquivos, qualquer agente segue o mesmo
método, e o Builder Mode do Mirror continua lendo o mesmo roadmap.

## Verification

O pull-candidates do Mirror lista CV1.DS1 a CV1.DS4 a partir do roadmap
convertido e recomenda a CV1.DS1.

## Follow-up

- Publicar o repositório para os colaboradores (feito em
  `89retreat/89books`).
- Decidir quem é o Navigator do trabalho dos colaboradores.
- Fechar as decisões abertas da CV1 durante a CV1.DS1.
