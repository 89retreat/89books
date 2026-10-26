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

Início. Nenhum código de produto ainda; o spike de reconhecimento e o
experimento do retrato estão em `spikes/reconhecimento/`.

O roadmap tem duas CVs. A
[CV1 A Primeira Estante Viva](roadmap/cv1-primeira-estante-viva/index.md) é um
MVP local: cada pessoa roda um script sobre as fotos da própria estante e
recebe um HTML bonito, com o retrato de si, para mandar ou publicar. A
[CV2 A Estante no Telegram](roadmap/cv2-a-estante-no-telegram/index.md) leva
a entrada e os movimentos para um bot, depois da retrospectiva da CV1.

O trabalho mais importante agora é fechar a `CV1.DS1` (validar as decisões da
TS2) e começar a `CV1.DS2`, a estante num arquivo.

## Architecture Premises

Detalhes em [decisions/records/](decisions/records/).

- **Interface (CV1):** um script Python local gera um HTML autocontido da
  estante. Sem bot, servidor, login ou hospedagem.
- **Compartilhamento:** a pessoa escolhe mandar o arquivo, publicar no GitHub
  Pages com endereço difícil de adivinhar, as duas coisas ou nenhuma.
- **Reconhecimento e retrato:** Claude Sonnet 5.5 via OpenRouter, só
  provedores sem retenção para treino. A estante aparece na hora e é
  corrigida aos poucos.
- **Metadados:** Open Library, ligando cada livro à obra; a estante não
  depende de capa.
- **CV2:** o bot do Telegram vira a porta, e um grupo dedicado recebe só o
  que cada pessoa escolhe compartilhar. A conversa acontece no Telegram, não
  dentro do produto.
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

- **Retrato de si**: a leitura que a IA faz da estante, em duas partes, a
  lente do leitor e os temas que se repetem.
- **Estante**: a composição autoral dos livros de alguém. Pode abranger
  vários lugares da casa. A estante física e a virtual são a mesma estante.
- **Movimento**: um acontecimento que dá vida à estante. Na CV2, apenas
  "comecei a ler" e "insight".
- **Insight**: um registro curto feito durante a leitura (texto, talvez a foto
  de um trecho), ligado a um livro.
- **Origem**: de onde um livro entrou na estante (foto, print do Kindle,
  seleção manual).
- **Dogfood**: usar o produto entre nós antes de abri-lo a outras pessoas.
