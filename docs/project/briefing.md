# Project Briefing

Contexto estável do 89 Livros. Premissas que não devem ser reexplicadas nem
rediscutidas a cada sessão.

## Purpose

Um produto para leitores ávidos, nascido da frustração de um grupo de amigos
com o Goodreads. Não pretende ser um catálogo melhor. Parte da descoberta de
que **visitar a estante de alguém é uma forma de encontrá-lo**: o conjunto de
livros revela a lente da pessoa, desperta perguntas e faz livros circularem
entre quem tem interesse.

Origem: Exploratory Story
[ES-001 A Estante como Retrato e Campo de Ressonância](exploration/es-001-a-estante-como-retrato/index.md).

## Current State

Início. Nenhum código de produto ainda; o spike de reconhecimento está em
`spikes/reconhecimento/`. O roadmap tem uma CV,
[CV1 A Primeira Estante Viva](roadmap/cv1-primeira-estante-viva/index.md): um
experimento de dogfood com o grupo de amigos que originou a conversa.

O trabalho mais importante agora é a `CV1.DS1`: o reconhecimento foi
validado (TS1), as decisões técnicas estão registradas (TS2) e falta o
esqueleto implantado (TS3).

## Architecture Premises

Decididas na `CV1.DS1`; detalhes em [decisions/records/](decisions/records/).

- **Interface:** web app pensado para celular; o bot do Telegram só envia
  (movimentos ao grupo e link de acesso).
- **Acesso:** link de uso único enviado pelo bot, só para quem está na lista
  de membros (ID do Telegram).
- **Stack:** Python + Django + HTMX, SQLite e fotos num volume, fila de
  reconhecimento no próprio banco, Fly.io em São Paulo, deploy pelo GitHub
  Actions.
- **Reconhecimento:** Claude Sonnet 5.5 via OpenRouter, só provedores sem
  retenção para treino, com revisão obrigatória pela pessoa.
- **Metadados:** Open Library, ligando cada livro à obra; a estante não
  depende de capa.
- A conversa acontece num grupo do Telegram, não dentro do produto.
- Cada livro na estante guarda a sua origem (foto, Kindle ou seleção manual).

## Product Premises

Ver [product/principles.md](../product/principles.md). Em resumo: a estante é o
centro; não se começa vazio; a foto da estante física é a presença da pessoa;
cada leitor revela a própria lógica; a conversa acontece onde as pessoas já
estão; a leitura não vira prestação de contas.

Público inicial: o grupo de amigos do dogfood, todos leitores para quem livro
rende assunto.

## Constraints

- Fotos de estantes e insights são pessoais. Não publicar, não usar em
  fixtures nem compartilhar fora do grupo sem consentimento.
- Nada de feed próprio, métricas de leitura, estrelas ou rankings na CV1.
- O experimento deve ser usável "de pronta" pelo grupo, sem instalação pesada.

## Operating Notes

O projeto usa o método **Ariad**. Comece pelo [AGENTS.md](../../AGENTS.md) e
pelo [guia local](../process/development-guide.md).

## Glossary

- **Estante**: a composição autoral dos livros de alguém. Pode abranger
  vários lugares da casa. A estante física e a virtual são a mesma estante.
- **Movimento**: um acontecimento que dá vida à estante. Na CV1, apenas
  "comecei a ler" e "insight".
- **Insight**: um registro curto feito durante a leitura (texto, talvez a foto
  de um trecho), ligado a um livro.
- **Origem**: de onde um livro entrou na estante (foto, print do Kindle,
  seleção manual).
- **Dogfood**: usar o produto entre nós antes de abri-lo a outras pessoas.
