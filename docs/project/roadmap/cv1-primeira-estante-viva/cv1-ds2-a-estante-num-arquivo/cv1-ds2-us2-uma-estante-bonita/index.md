---
code: CV1.DS2.US2
level: User Story
status: Active
status_reason: puxada pelo Navigator com o design aprovado nos protótipos
updated: 2026-10-26
related:
  - ../cv1-ds2-us1-gerar-minha-estante/index.md
  - ../../../../decisions/records/2026-10-24T2013Z-acesso-do-grupo.md
  - ../../../../exploration/es-002-a-estante-num-arquivo/artifacts/product-design-proposal.md
---

[< Parent](../index.md)

# CV1.DS2.US2 — Uma estante bonita, mesmo sem capas

**Status:** Active
**Type:** User Story

---

## User Story

As uma pessoa do grupo que gerou a própria estante,
I want que a página me apresente como leitor, com os livros organizados pelos
momentos em que recorro a eles,
So that eu tenha vontade de mostrar a estante, e quem a visita entenda quem eu
sou, sem rolar uma lista sem fim.

## Outcome

O `shelf.html` passa a ter o design aprovado nos protótipos de 2026-10-26
(v1 a v7, com as fotos do Lula). O retrato deixa de ser um bloco separado da
lista: os temas viram as prateleiras da estante.

## Premissa

O HTML é um artefato de validação entre os fundadores, aberto num navegador
de verdade. O produto final será compartilhado por URL. Por isso:

- a página pode depender de JavaScript para o layout;
- a pré-visualização do Mac e a do WhatsApp estão fora do escopo;
- não otimizamos mais o tamanho do arquivo além do razoável.

## Design aprovado

**Abertura**

- Mosaico das fotos. A primeira foto, ou a indicada em `cover_photo` no
  `config.toml`, fica grande; as demais ficam menores ao redor. Tocar numa
  foto amplia; tocar de novo ou Esc fecha. O mosaico se adapta a qualquer
  número de fotos. No celular, mostra no máximo cinco, e as outras aparecem ao
  ampliar.
- Título "A estante de {nome}", com o nome em destaque.
- A lente, em primeira pessoa, com capitular.

**Prateleiras**

- Cada tema do retrato é uma prateleira: um módulo com fundo próprio, numeral
  romano grande com serifa, título e parágrafo, e os livros em cima de tábuas.
- O título é a situação que leva a pessoa à prateleira, em primeira pessoa:
  "Quando busco pensar o Brasil a partir da negritude". Tudo é escrito pela
  pessoa para quem a visita ("eu", "minha estante").
- O retrato distribui os livros entre os temas na mesma chamada ao modelo.
  Os que sobram vão para uma última prateleira, "Quando não procuro nada em
  particular".
- Os livros são lombadas desenhadas: cor de uma paleta contemporânea derivada
  do título, altura variada, espessura pelo tamanho do título, frisos e volume.
  Lombadas claras levam texto escuro.
- Ficam de frente, com capa, os livros que o parágrafo do tema cita. Cada capa
  tem inclinação própria, em intensidade e direção, estável entre gerações. Na
  última prateleira, algumas capas de frente só dão ritmo.
- Os livros se distribuem em fileiras que cabem na largura do módulo, cada uma
  com a sua tábua. Uma última fileira muito curta, e as fileiras além de três
  na última prateleira, ficam atrás de "Expandir… mais N livros", que vira
  "Recolher".
- Capa que não carrega ou vem vazia vira lombada.

**Tipografia e cor**

- Fundo quase branco, um único destaque em laranja-terracota (nome, capitular,
  numerais, "Expandir…"), tábuas em grafite.
- Títulos das prateleiras em Newsreader itálica, embutida no arquivo (licença
  OFL). Numerais em Georgia. Texto corrido com serifa.

**Telas grandes**

- Duas colunas: prateleiras com mais de oito livros na principal, com o texto
  em duas colunas; prateleiras pequenas numa coluna lateral, com o numeral
  sobre o título e o título menor.
- Se a coluna lateral ficar mais alta, a última prateleira dela desce para a
  principal, desde que isso reduza o vão.
- A última prateleira ocupa a largura toda.
- Abaixo de 860 px, tudo volta a uma coluna, na ordem do retrato.

## Acceptance Behavior

```text
Given uma pasta de fotos já reconhecida
When rodo `uv run shelf <folder>`
Then o `shelf.html` abre com o mosaico, o nome e a lente em primeira pessoa
And cada tema é uma prateleira com numeral, título em forma de situação, parágrafo e os livros do tema em lombadas
And os livros citados no parágrafo aparecem de frente, quando têm capa
And os livros sem tema aparecem na última prateleira, com "Expandir…"
And a página funciona no Chrome e no Safari, no computador e no celular
```

```text
Given um `config.toml` com `cover_photo = "photo-03.jpg"`
When gero a estante
Then essa foto é a maior do mosaico
```

## Scope

- Novo prompt do retrato: lente e temas em primeira pessoa, título como
  situação e distribuição dos livros entre os temas.
- Novo template com mosaico, prateleiras, lombadas, capas de frente, fileiras
  com tábua, "Expandir…" e as duas colunas.
- `cover_photo` opcional no `config.toml`.
- Fonte Newsreader itálica embutida.

## Out Of Scope

- Pré-visualização do Mac e do WhatsApp (premissa acima).
- Escolher a edição certa na Open Library, preferir edições em português e
  medir o Google Books: com as lombadas, a falta de capa deixou de ser problema
  visual. Capas erradas, como a do sumário no protótipo, ficam para a correção
  da US3.
- Cache do reconhecimento, correção pelo `books.yaml` e `--new-portrait` (US3).
- Publicação (DS3).

## Validation

Navigator: gerar uma estante e abrir no Chrome do computador e do celular,
reconhecendo o design aprovado nos protótipos.
