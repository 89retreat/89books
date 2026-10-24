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

Início. Nenhum código ainda. O roadmap tem uma CV,
[CV1 A Primeira Estante Viva](roadmap/cv1-primeira-estante-viva/index.md): um
experimento de dogfood com o grupo de amigos que originou a conversa.

O trabalho mais importante agora é a `CV1.DS1`, que verifica se uma foto de
estante vira uma lista confiável de livros e fecha as decisões técnicas.

## Architecture Premises

Ainda em aberto. Ver as decisões com `status: Open` em
[decisions/records/](decisions/records/). Premissas já assumidas:

- os metadados dos livros vêm da Open Library, normalizando título, autor e
  capa;
- o reconhecimento de livros em fotos usa um modelo de visão;
- a conversa acontece num grupo do Telegram, não dentro do produto;
- cada livro na estante guarda a sua origem (foto, Kindle ou seleção manual).

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
