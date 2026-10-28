---
id: ES-002
status: Promoted
opened: 2026-10-26
updated: 2026-10-26
source:
  - validação da CV1.DS1.TS2 (decisões de interface, acesso e stack)
  - sessão em Explorer Mode do Mirror Mind (jornada 89-livros, história "O Telegram como Porta da Estante", id d6435720)
  - experimento do retrato com o Lula
attractor: O Retrato de Si
promoted_to: CV1 A Primeira Estante Viva (reorganizada) e CV3 A Estante no Telegram (hoje CV4)
refinement_request:
related:
  - ../es-001-a-estante-como-retrato/index.md
  - ../../roadmap/cv1-primeira-estante-viva/index.md
  - ../../roadmap/cv4-a-estante-no-telegram/index.md
  - ../../roadmap/cv1-primeira-estante-viva/cv1-ds1-fundacao/cv1-ds1-ts2-registrar-decisoes-tecnicas-da-cv1/index.md
  - ../../../../spikes/reconhecimento/relatorio.md
---

# ES-002 — A Estante num Arquivo

## Current Story

O primeiro MVP é local. Cada pessoa põe fotos da estante ou das prateleiras
numa pasta, configura a chave do OpenRouter num arquivo e roda um script
Python. O resultado é um HTML autocontido e bonito da sua estante: as fotos,
uma capa escolhida, os livros reconhecidos e um **retrato de si** em duas
partes, a lente que a estante revela e os temas que se repetem.

O desenho parte do prêmio que a pessoa recebe pelo esforço do input. Não há
bot, servidor, login nem hospedagem. A estante aparece na hora, com a leitura
da IA, e é corrigida aos poucos: a pessoa apaga linhas de um arquivo de livros
e roda de novo, com o reconhecimento em cache. O retrato pode ser gerado outra
vez, mas não é editado; recusar um retrato que não a representa basta.

A estante circula como arquivo, como link no GitHub Pages ou das duas formas,
e a pessoa decide. Cerca de 40% das obras não têm capa na Open Library, então
o visual dos livros sem capa é o centro do trabalho de beleza.

O Telegram, que abriu esta exploração, continua no horizonte como a porta de
entrada da CV seguinte, com a forma já desenhada aqui.

## Initial Signal

Ao validar a CV1.DS1.TS2, o Navigator se inclinou a desfazer a decisão
proposta pelo Driver (web app como interface, bot só para enviar) e levar toda
a entrada para o Telegram, com a página web só para ver a estante.

## Thickening Timeline

### 2026-10-26 — O Telegram como porta

Entrada e movimentos pelo bot, estante como página. O ganho é menos atrito; a
tensão, revisar dezenas de livros num chat. Hipótese do Driver: Mini Apps do
Telegram para revisão e estante.

### 2026-10-26 — A amizade vive no WhatsApp (correção)

O Telegram entrou na ES-001 por ser fácil de construir, não por ser o lugar
social do grupo. O Navigator deixou de lado levar os movimentos a grupos
sociais já instituídos e fixou um critério único: remover atritos.

### 2026-10-26 — Telegram como requisito; estante antes da revisão

Todos do grupo usam Telegram, e novos usuários precisarão ter. A estante
aparece na hora com a leitura da IA e é corrigida aos poucos. A revisão
obrigatória, registrada como consequência da TS1, deixa de ser etapa de
entrada e se dissolve na própria estante.

### 2026-10-26 — O retrato de si

A primeira leitura da IA vai além de reconhecer títulos e devolve um retrato:
a lente do leitor e os temas que se repetem. Reconecta o produto ao atrator da
ES-001, a estante como retrato.

### 2026-10-26 — O bot em dois lugares

Conversa privada com cada pessoa (entrada, retrato, insights, comecei a ler) e
um grupo dedicado onde o bot publica só o que a pessoa escolhe. Apresentar a
estante ao grupo é um gesto dela. A estante abre também no navegador comum.

### 2026-10-26 — Primeiro MVP com o bot

Fotos pelo bot, sem distinguir estante de prateleira; página com carrossel,
botão para definir a capa, lista com botão de remover, retrato regenerável e
link para visitar.

### 2026-10-26 — O retrato funciona (experimento)

O Lula se reconheceu no retrato feito à mão. A pergunta final não ajudou e
saiu.

### 2026-10-26 — A estante num arquivo

O Navigator simplificou o MVP a partir do output: pasta de fotos, chave,
script e um HTML bonito. Cada colaborador roda o seu, porque todos são
técnicos; o modo concierge foi descartado. HTML autocontido; compartilhamento
por arquivo ou GitHub Pages, à escolha da pessoa.

## Attractors and Tensions

- **O Retrato de Si** (confirmado pelo experimento): a pessoa se reconhece na
  leitura que a estante faz dela.
- **A estante como prêmio do input** (confirmado): o esforço de entrada se
  mede pelo que a pessoa recebe.
- Tensão: beleza da estante com ~40% dos livros sem capa.
- Tensão: compartilhar por link expõe fotos da casa a quem tiver o endereço.
- Tensão: corrigir aos poucos sem que leituras erradas cheguem a quem visita.

## Experiments

**O retrato do Lula, feito à mão** (2026-10-26, concluído). Retrato gerado
com `spikes/reconhecimento/retrato.py` (Sonnet 5.5) a partir dos 146 itens que
o spike extraiu das fotos do Lula, com os erros de leitura incluídos. Custou
US$ 0,016 e foi enviado pelo Alisson, com consentimento do Lula, sem página
nem bot. Resultado: ele se reconheceu; a pergunta final não ajudou e saiu do
prompt. Não testado: o comprimento do retrato no celular e um segundo leitor.
O retrato fica fora do repositório.

## Carry Forward Notes

- Fechar a CV1.DS1.TS2 sem aceitar as decisões de interface, acesso e
  stack/hospedagem; substituí-las por registros coerentes com o MVP local.
- No registro de reconhecimento, trocar "revisão obrigatória" por "correção
  gradual".
- Reorganizar a CV1 em torno do script: gerador do HTML, visual para livros
  sem capa, correção por arquivo, retrato regenerável e, depois, publicação no
  GitHub Pages.
- Levar para uma CV seguinte o bot, o grupo dedicado e os movimentos, com as
  respostas desta exploração: grupo do Telegram dedicado; compartilhar um
  insight é sempre escolha da pessoa.
- Decisão aberta: publicar no repositório da org 89retreat ou no repositório
  pessoal de cada um.

## Candidate / Promotion

Promovida para Delivery em 2026-10-26 por decisão do Navigator (Alisson):

- a [CV1](../../roadmap/cv1-primeira-estante-viva/index.md) foi reorganizada
  em torno do script: CV1.DS2 A estante num arquivo e CV2.DS2 (hoje CV3.DS1) Estante
  visitável; a CV1.DS1.TS3 (esqueleto implantado) foi descartada;
- a [CV3, hoje CV4,](../../roadmap/cv4-a-estante-no-telegram/index.md) recebeu o bot, o
  grupo dedicado e os movimentos (a antiga CV1.DS4 virou CV3.DS2, hoje CV4.DS2);
- as decisões da CV1.DS1.TS2 foram reescritas para o MVP local; grupo do
  Telegram e privacidade dos insights ficaram `Decided`; a publicação no
  GitHub Pages abriu um registro novo.

Os documentos gerados pelo Explorer Mode do Mirror Mind estão em
[artifacts/](artifacts/index.md); o `product-design-proposal.md` foi reescrito
pelo Driver na promoção.

## Kept-for-Later Signals

- Levar os movimentos a grupos sociais já instituídos, como o WhatsApp do
  grupo.
- Mini Apps do Telegram para a estante.
- Como a estante sinaliza o que a IA não teve certeza.
- Print do Kindle e seleção manual como portas de entrada.

## Archive Notes
