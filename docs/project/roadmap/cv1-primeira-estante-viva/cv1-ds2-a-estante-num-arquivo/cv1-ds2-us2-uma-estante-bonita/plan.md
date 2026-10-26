[< Story](index.md)

# Plan — CV1.DS2.US2

## Objective

Levar ao comando `shelf` o design aprovado nos protótipos: mosaico, lente em
primeira pessoa e os temas do retrato como prateleiras de lombadas, com os
livros citados de frente.

## Pull

Puxada em 2026-10-26, logo após o Navigator validar a US1. O design foi
desenhado antes, em sete protótipos sobre a estante do Lula, e aprovado pelo
Navigator.

## Prepare

- Os protótipos estão fora do repositório, em `/tmp/estante-prototipo/`
  (`montar7.py` e `prototipo-v7.html`). Eles servem de referência para o CSS e
  o JavaScript, e não são copiados como estão.
- O código da US1 já separa o retrato (`portrait`), a página (`page`) e o
  template. A US2 troca o prompt do retrato, o template e a preparação dos
  dados da página.
- Premissa registrada na story e no registro de
  [acesso](../../../../decisions/records/2026-10-24T2013Z-acesso-do-grupo.md):
  o HTML é um artefato de validação entre fundadores; o produto final será
  compartilhado por URL.

## Scope

- `portrait`: novo prompt. O modelo devolve a lente e de três a seis temas,
  tudo em primeira pessoa. Cada tema traz um título em forma de situação
  ("Quando…", até 60 caracteres), um parágrafo que cita livros entre
  asteriscos e os números dos livros que pertencem a ele. A lista vai numerada
  para o modelo. A leitura da resposta descarta números inválidos ou repetidos
  e mantém a ordem dos temas.
- Novo módulo `shelves`, puro e testável, que prepara a página:
  - distribui os livros pelas prateleiras, com uma última prateleira para os
    que sobram;
  - lombada: cor de uma paleta fixa a partir do título, se é clara, altura,
    espessura pelo tamanho do título e rótulo truncado;
  - livro de frente: citado no parágrafo e com capa; na última prateleira, um
    a cada nove com capa;
  - inclinação e elevação estáveis a partir do título, nas duas direções;
  - lugar de cada prateleira em telas grandes: lateral até oito livros,
    principal acima disso, largura toda para a última.
- `config`: `cover_photo` opcional no `config.toml`, com erro claro se a foto
  não existir na pasta.
- `photos`: tamanho próprio para a página (1000 px), separado do enviado ao
  modelo (1600 px). A foto de capa vai primeiro.
- Template novo, com CSS e JavaScript embutidos:
  - mosaico para qualquer número de fotos, com ampliação e navegação entre
    fotos; no celular, até cinco visíveis;
  - prateleiras, lombadas e capas de frente;
  - fileiras com tábua montadas pela largura real e "Expandir…"/"Recolher";
  - capa que falha ou vem vazia vira lombada;
  - duas colunas com balanceamento acima de 860 px e uma coluna abaixo.
- Fonte Newsreader itálica embutida: o arquivo `woff2` (recorte latin) fica
  no pacote, com a licença OFL ao lado, e entra no HTML em base64.
- Guia de teste, README (o que a página mostra) e `config.toml` de exemplo
  com `cover_photo`.

## Non-Goals

- Pré-visualização do Mac e do WhatsApp.
- Edição certa ou em português na Open Library, Google Books e detecção de
  capas erradas (como o sumário): a correção é da US3.
- Cache do reconhecimento, `books.yaml` editável e `--new-portrait` (US3).
- Publicação (DS3).

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

## Validation Route

- Automático: `uv run pytest` e `uv run ruff check . && uv run ruff format --check .`.
  Testes novos cobrem a leitura do retrato com livros por tema, o módulo
  `shelves` (distribuição, sobras, livros de frente, determinismo das cores e
  inclinações, lugar das prateleiras), `cover_photo` e a página (estrutura das
  prateleiras, escape, fonte embutida, privacidade).
- Driver: gerar de novo a estante do Lula numa pasta fora do repositório
  (cerca de US$ 0,10, porque o reconhecimento ainda não tem cache) e conferir
  no navegador em 1440, 1200, 900 e 390 px: mosaico, ampliação, fileiras com
  tábua, "Expandir…", colunas e capas que falham.
- Navigator: abrir a estante gerada no Chrome do computador e do celular.
  - Passa: reconhece o design aprovado nos protótipos, agora gerado pelo
    comando.
  - Falha: prateleiras sem livros ou sem título, layout quebrado em alguma
    largura, ou texto que não está em primeira pessoa.

E2E decision: o teste de ponta a ponta automatizado continua com rede
simulada; o layout depende do navegador e é conferido pelo Driver com o
navegador automatizado.

## Implementation Contract

- TDD nos módulos com comportamento (`portrait`, `shelves`, `config`,
  `page`). O JavaScript de layout é conferido no navegador.
- Use uv run for Python commands and tests.
- Nenhuma foto, estante gerada ou chave entra no git.
- Commit só com arquivos da story; mensagem em inglês explicando o porquê.
  Sem push sem comando do Navigator.

## Stop Conditions

- scope_change_detected
- plan_rule_conflict
- failing_required_check_without_clear_fix
- navigator_decision_needed

## Approval Gate

- active checkpoint: `after_plan`
- pending confirmation: `navigator_approval`, satisfeita pela autoridade de
  plano da cadência `accelerated` (2026-10-26), com parada fixa na validação
  do Navigator.
