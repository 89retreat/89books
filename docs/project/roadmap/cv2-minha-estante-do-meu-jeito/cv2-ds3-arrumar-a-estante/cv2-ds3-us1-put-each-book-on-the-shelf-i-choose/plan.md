[< Story](index.md)

# Plan — CV2.DS3.US1 Put each book on the shelf I choose

## Pull

Puxada pelo Navigator em 2026-10-28 depois da validação e do fechamento de
CV2.DS2.US2. Corrigir livros já funciona; o próximo gesto é decidir onde cada
livro mora e em que ordem aparece.

## Prepare

### Estado atual

- `ShelfFile.shelves` e `ShelfSection.books` já são listas ordenadas no contrato
  v1; parse e dump preservam sua ordem.
- `shelves_from_file` percorre seções e livros na ordem da fonte, sem aplicar o
  agrupamento automático por autor usado na criação da CV1.
- `draw` já reflete uma inversão manual das prateleiras e salva a fonte mudada.
- Seções vazias continuam na página com título e texto.
- O núcleo ainda não oferece operações nomeadas para mover livro, criar,
  reordenar ou remover prateleira numa futura UI.
- A detecção atual de fechamento considera qualquer última seção sem texto
  como `rest`. Assim, uma prateleira vazia criada pela pessoa no fim recebe
  silenciosamente o visual especial e perde o numeral.

### Decisões da fatia

1. **A ordem da fonte é a ordem autoral:** nenhuma regra volta a agrupar livros
   ou prateleiras depois que existe `shelf.yaml`.
2. **Mover significa mover o objeto inteiro:** título, autores, `known_as`,
   `hidden`, `face`, capa e provenance viajam juntos.
3. **Posições internas são zero-based:** `None` significa anexar; uma posição
   explícita é o índice da lista final depois da remoção, inclusive em
   reordenação dentro da mesma prateleira.
4. **Remover prateleira é seguro:** a operação pura só remove seção vazia;
   livros nunca são apagados implicitamente.
5. **Fechamento é reconhecível:** só a última seção sem texto cujo título é
   exatamente `E mais livros que já me acompanharam` recebe `rest=true`.
   Uma seção criada ou renomeada pela pessoa é regular.
6. **Sem novo verbo terminal:** a superfície atual continua sendo editar YAML,
   rodar `check`, `draw` e `open`.

## Scope

### Characterization of authored order

Adicionar testes que provem:

- ordem das seções gera numerais e `order` na mesma sequência;
- ordem dos livros em cada seção é literal, mesmo para autores iguais;
- mover uma entrada completa no YAML muda posição/prateleira na página;
- seções vazias são renderizadas;
- uma última seção customizada sem texto é regular;
- a seção canônica de fechamento só é especial quando permanece por último.

A distribuição responsiva entre colunas continua sendo apresentação: os
numerais e a ordem responsiva carregam a sequência autoral. A story não refaz o
algoritmo de balanceamento visual.

### Pure operations for a future UI

Adicionar ao núcleo:

```python
move_book(
    shelf,
    from_shelf_index,
    book_index,
    to_shelf_index,
    position=None,
) -> ShelfFile

add_shelf_section(shelf, title, *, text="", position=None) -> ShelfFile
move_shelf_section(shelf, shelf_index, position) -> ShelfFile
remove_shelf_section(shelf, shelf_index) -> ShelfFile
```

Contrato:

- todas retornam novas cópias sem mutar a fonte;
- índices negativos ou fora do alcance levantam `IndexError`;
- posição de inserção aceita `0..len(lista)` e `None` para anexar;
- `move_book` preserva exatamente o `ShelfBook` completo;
- origem e destino iguais reordenam dentro da mesma lista após remover o item;
- adicionar exige título não vazio e texto textual;
- mover seção preserva a seção completa;
- remover seção não vazia levanta `ValueError` com mensagem clara;
- seções não tocadas e livros não movidos podem manter identidade de objeto.

### Closing-shelf semantics

Trocar a heurística `last and not section.text` por uma condição que também
exija `section.title == REST_TITLE`. Isso mantém a seção gerada pela CV1 como
fechamento, mas impede que uma seção autoral vazia seja reinterpretada.

Não adicionar um campo `rest` ao formato v1 nesta story.

### Documentation

Documentar em `GETTING_STARTED.md` e `my-bookshelf/README.md`:

- mover o bloco inteiro do livro, não apenas `title`;
- ordem das listas é a ordem da estante;
- criar uma seção com `title`, `text` opcional e `books`;
- remover somente uma seção vazia para não perder livros;
- executar `check`, `draw`, `open`, todos gratuitos.

## Non-Goals

- Comando `move`, seletor por título ou edição interativa.
- Drag-and-drop, servidor ou API HTTP.
- Excluir uma prateleira junto com seus livros.
- Decidir `face`, `cover_photo`, títulos/textos ou pedir outro retrato.
- Alterar a classificação wide/side ou o balanceamento das colunas.
- Agrupar livros automaticamente por autor depois da edição.
- Mudar o schema ou a versão do YAML.

## Implementation Approach

1. Caracterizar primeiro a ordem literal já entregue pelo renderer.
2. Escrever testes vermelhos para seção customizada final sem texto e corrigir
   apenas a heurística de `rest`.
3. Escrever testes das quatro operações puras, incluindo mesma origem/destino,
   metadados completos, posições-limite e remoção segura.
4. Adicionar um E2E de cliente: editar a fonte, mover livro/seção, `check` e
   `draw`, provar ordem no HTML e snapshot da fonte desenhada.
5. Atualizar documentação sem criar comando novo.
6. Validar numa cópia descartável e parar no checkpoint do Navigator.

## Test Strategy

```bash
uv run pytest tests/test_core.py tests/test_shelves.py tests/test_page.py tests/test_cli.py tests/test_shelf_file.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Casos obrigatórios:

- duas obras do mesmo autor permanecem separadas quando o arquivo assim manda;
- mover entre seções preserva todos os campos, inclusive `hidden`, `face`,
  capa e provenance;
- mover dentro da mesma seção respeita posição final;
- anexar com `position=None` funciona para livro e seção;
- posições negativas, seção/livro ausente e posição maior que o comprimento
  falham sem mutação;
- adicionar seção em começo, meio e fim preserva as demais;
- reordenar seção move o objeto inteiro;
- remover seção vazia funciona; remover não vazia falha;
- seção customizada final sem texto recebe numeral e estilo regular;
- seção canônica final continua sem numeral e com estilo `full`;
- edição válida é desenhada gratuitamente e salva snapshot; erro de YAML ainda
  preserva a página anterior;
- core não escolhe pasta, imprime ou lê terminal.

## Validation Route

Criar `/tmp/89books-ds3-us1-validation` como cópia descartável de uma estante
já existente, sem abrir nem comparar versões reais:

1. escolher um livro com metadados visíveis e mover seu bloco YAML completo
   para o início de outra seção;
2. rodar `check`, `draw`, `open` e confirmar livro, prateleira e posição;
3. criar no fim uma seção `Uma prateleira minha`, sem texto, mover o livro para
   ela e confirmar que recebe numeral/visual regular, não o fechamento;
4. mover essa seção para o começo e confirmar ordem/numerais;
5. mover o livro de volta, remover a seção vazia e redesenhar;
6. confirmar que cada redraw foi gratuito e que `history` ganhou as fontes
   desenhadas, sem ler ou comparar seus conteúdos.

- **Observação esperada:** página segue seção e posição do YAML; livro conserva
  identidade/capa; seção customizada não vira fechamento por acidente.
- **Passa:** todos os movimentos aparecem, snapshots são registrados e nenhum
  catálogo, chave ou modelo é usado.
- **Falha:** agrupamento automático vence a fonte, metadata some, livros são
  apagados ao remover seção, ou a seção customizada recebe semântica de rest.

## Product Principles Preserved

- **Cada leitor revela a própria lógica:** ordem e agrupamento pertencem à
  pessoa, não ao algoritmo.
- **A última palavra é de quem lê:** nenhuma regra reorganiza a fonte editada.
- **Nada se perde:** remoção pura recusa seção com livros; draw registra fonte.
- **Gastar é escolha:** check/draw/open continuam offline e gratuitos.
- **Terminal como protótipo:** operações puras preparam drag-and-drop futuro.

## Risks and Ambiguities

- Em desktop, o layout distribui seções entre colunas para equilibrar alturas;
  numerais e ordem responsiva continuam autorais. Reescrever esse layout seria
  outra story.
- A seção de fechamento ainda é reconhecida pelo título canônico, não por um
  campo explícito. Se pessoas quiserem várias seções especiais, o schema pode
  evoluir depois.
- A edição manual pode apagar uma seção com livros; a operação futura é segura,
  mas YAML continua poderoso. Histórico e restore são a proteção existente.
- `position` é API interna zero-based; não vira conceito exposto no terminal.

## Stop Conditions

- A solução exigir novo campo ou migração do YAML v1.
- A story começar a implementar frente/lombada, foto ou textos.
- O renderer voltar a agrupar por autor ou reescrever a ordem.
- A operação de remoção apagar livros implicitamente.
- A validação exigir catálogo, modelo, chave ou histórico real.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: pending
- Approved on: pending
