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

A [CV1 A Primeira Estante Viva](roadmap/cv1-primeira-estante-viva/index.md)
está concluída (2026-10-28): cada fundador clonou o repositório público, pôs as
fotos em `my-bookshelf/`, rodou `uv run shelf` e recebeu a própria estante, um
HTML com fotos, livros, autores e o retrato de si.

O trabalho agora é a
[CV2 Minha estante, do meu jeito](roadmap/cv2-minha-estante-do-meu-jeito/index.md):
a pessoa ajusta a estante editando o `shelf.yaml` e redesenhando a página, sem
pagar de novo. A primeira entrega é a CV2.DS1, que faz do arquivo a fonte da
estante. Depois vêm a [CV3](roadmap/cv3-a-estante-visitavel/index.md),
estante visitável por link, e a [CV4](roadmap/cv4-a-estante-no-telegram/index.md),
a porta para quem não usa o terminal.

O caminho de produto (fundadores e amigos técnicos pelo terminal, depois
pessoas não técnicas) está em [direction.md](../product/direction.md).

## Architecture Premises

Detalhes em [decisions/records/](decisions/records/).

- **Interface (CV1, CV2):** um comando Python local, `uv run shelf`, sobre a
  pasta `my-bookshelf/`. Sem bot, servidor, login ou hospedagem.
- **Núcleo e terminal:** o terminal é um cliente fino. As operações da
  estante ficam num núcleo que não pergunta nem imprime, para que um servidor
  o rode sem mudança
  ([decisão](decisions/records/2026-10-28T1400Z-terminal-como-cliente-fino.md)).
- **A fonte da estante (CV2):** o `my-bookshelf/shelf.yaml`, com versão.
  Gerar a partir das fotos é pago e acontece uma vez; desenhar a página é
  grátis. Todo comando que reescreve o arquivo guarda uma versão em
  `history/`
  ([decisão](decisions/records/2026-10-28T1400Z-o-arquivo-da-estante-como-fonte.md)).
- **Compartilhamento:** hoje, a pessoa manda o arquivo HTML. O arquivo é
  temporário; fora do grupo, a estante será compartilhada por link (CV3).
- **Reconhecimento e retrato:** Claude Sonnet 5.5 via OpenRouter, só
  provedores sem retenção para treino, com a chave de cada pessoa. A estante
  aparece pronta e é corrigida aos poucos.
- **Metadados:** Open Library, ligando cada livro à obra, e Google Books como
  segundo catálogo, com chave opcional.
- **CV4:** a porta para quem não usa o terminal (bot do Telegram ou aplicação
  web, em decisão aberta) e os movimentos num grupo dedicado do Telegram. A
  conversa acontece no Telegram, não dentro do produto.
- Cada livro na estante guarda a sua origem.

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
- Nada de feed próprio, métricas de leitura, estrelas ou rankings.
- O experimento deve ser usável "de pronta" pelo grupo, sem instalação pesada:
  um clone, o guia e um comando.
- Toda a superfície do terminal (comandos, mensagens, guia, chaves do
  `shelf.yaml`) é em inglês; a estante e o retrato, em português do Brasil.

## Operating Notes

O projeto usa o método **Ariad**. Comece pelo [AGENTS.md](../../AGENTS.md) e
pelo [guia local](../process/development-guide.md).

## Glossary

- **Retrato de si**: a leitura que a IA faz da estante, em duas partes, a
  lente do leitor e os temas que se repetem.
- **Estante**: a composição autoral dos livros de alguém. Pode abranger
  vários lugares da casa. A estante física e a virtual são a mesma estante.
- **Movimento**: um acontecimento que dá vida à estante. Na CV4, apenas
  "comecei a ler" e "insight".
- **Insight**: um registro curto feito durante a leitura (texto, talvez a foto
  de um trecho), ligado a um livro.
- **Origem**: de onde um livro entrou na estante (foto, print do Kindle,
  seleção manual).
- **`shelf.yaml`**: o arquivo que é a fonte da estante de cada pessoa, a
  partir da CV2. Editá-lo e rodar `draw` muda a página.
- **Gerar / desenhar**: gerar lê as fotos e escreve o retrato (pago, uma
  vez); desenhar escreve a página a partir do `shelf.yaml` (grátis, sempre).
- **Versão**: uma cópia do `shelf.yaml` em `my-bookshelf/history/`, guardada
  antes de cada reescrita.
- **Núcleo**: as operações da estante, sem terminal, que um servidor também
  roda.
- **Dogfood**: usar o produto entre nós antes de abri-lo a outras pessoas.
