[< Story](index.md)

# Plan — CV2.DS2.US1 Hide books from my shelf

## Pull

Puxada em 2026-10-28 depois das cinco stories da DS1. A validação da US1
registrou um livro identificado incorretamente; esconder é a menor correção
possível e já exercita a promessa central da CV2: a pessoa tem a última palavra
sem apagar dados nem pagar de novo.

## Prepare

### Estado atual

- O contrato v1 já aceita `hidden: true` e preserva também `false` explícito.
- `shelves_from_file` já pula livros com `hidden is True` antes de montar
  prateleiras e calcular autores frequentes.
- O painel já mostra total, visíveis e escondidos; `check` já valida booleanos;
  `draw` conta apenas livros visíveis e guarda a fonte alterada no histórico.
- Esse comportamento ainda não tem contrato de página/E2E próprio, instrução
  clara para a pessoa ou operação nomeada no núcleo para uma futura interface.

### Decisões da fatia

- **Esconder não é apagar:** o objeto permanece na mesma posição do YAML.
- **A página não reescreve prosa:** capa/lombada e contribuição para autores
  somem; lente e texto de prateleira permanecem exatamente como a pessoa
  escreveu, mesmo que citem o título.
- **Sem novo verbo:** nesta versão a pessoa edita `hidden: true` e usa os
  comandos já existentes `check`, `draw`, `open`, `history` e `restore`.
- **Operação de produto nomeada:** uma futura UI não deve manipular dataclasses
  diretamente; o núcleo oferece funções puras de esconder e mostrar por
  posição.

## Scope

### Núcleo reutilizável

Adicionar em `shelf.core`:

- `hide_book(shelf, shelf_index, book_index) -> ShelfFile`;
- `show_book(shelf, shelf_index, book_index) -> ShelfFile`.

As funções:

- devolvem uma nova estrutura e não alteram a entrada;
- preservam todos os campos, ordem e provenance;
- `hide_book` define `hidden=True`;
- `show_book` remove a marca (`hidden=None`) para manter o arquivo limpo;
- deixam `IndexError` sinalizar uma posição inexistente, sem terminal, arquivo
  ou ambiente.

O terminal não ganha comando novo. Essas operações são a fronteira que uma
aplicação web ou botão futuro poderá chamar.

### Rendering contract

- Livros `hidden: true` não chegam ao layout de capas/lombadas.
- Eles não entram em `frequent_authors`, portanto não sustentam “Quem mais
  mora aqui”.
- `hidden: false` e campo ausente continuam visíveis.
- Esconder não reordena os visíveis restantes; mostrar devolve a posição
  original descrita pelo YAML.
- Uma prateleira pode ficar visualmente vazia; título e texto pertencem à
  pessoa e não são apagados automaticamente nesta story.

### Existing command integration

- `check`: aceita `true`/`false`, rejeita outros valores com linha.
- status: total inclui escondidos; visível e escondido são separados.
- `draw`: saída informa somente a quantidade visível e salva a fonte alterada
  antes de desenhar.
- `history`/`restore`: preservam o campo como bytes, sem comparação automática.

### Documentation

- Adicionar ao `GETTING_STARTED.md` e `my-bookshelf/README.md` um exemplo curto:

  ```yaml
  - title: Um livro que não quero mostrar
    authors: [Autora]
    hidden: true
  ```

- Explicar: tirar a linha traz o livro de volta; `hidden: false` também é
  visível; o texto da prateleira não é reescrito.
- Atualizar README e help somente se necessário; não criar comando inexistente.

## Non-Goals

- Comando `shelf hide`, seletor por título ou editor interativo.
- IDs estáveis de livro ou mudança do formato v1.
- Remover menções do livro em prosa livre.
- Excluir prateleiras vazias.
- Corrigir título, autor, capa ou reconhecimento (US2).
- Comparar versões reais do histórico.

## Implementation Approach

1. Escrever testes de página que falham se livro escondido produzir capa,
   lombada ou autor frequente.
2. Caracterizar `hidden: false`, campo ausente, ordem e prateleira vazia.
3. TDD das operações puras `hide_book` e `show_book`, incluindo imutabilidade
   e preservação de metadados.
4. Ajustar somente o código que os contratos revelarem necessário; o filtro
   existente pode já satisfazer parte da story.
5. Adicionar E2E sintético: editar YAML, check, draw, status, history, remover
   marca e draw novamente, sem chaves.
6. Atualizar documentação e validar visualmente numa cópia descartável.

## Test Strategy

```bash
uv run pytest tests/test_core.py tests/test_page.py tests/test_shelves.py tests/test_shelf_file.py tests/test_cli.py tests/test_status.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Casos obrigatórios:

- livro escondido não aparece como spine/face no HTML;
- autor com dois livros deixa “Quem mais mora aqui” quando um deles fica
  escondido;
- `hidden: false` e ausência continuam visíveis;
- ordem relativa dos livros visíveis não muda;
- prateleira com todos escondidos preserva título/texto, mas não livros;
- hide/show retornam cópia, preservam campos e não mutam a fonte;
- check aponta linha de valor não booleano;
- painel mostra total/visível/escondido e draw reporta só visíveis;
- draw alterado cria versão; draw sem nova mudança não duplica;
- nenhuma chave, rede ou serviço pago é tocado.

## Validation Route

Criar uma cópia descartável da estante de uma foto, sem comparar conteúdos de
histórico:

1. A pessoa escolhe um livro visível e adiciona `hidden: true`.
2. Roda `check`, `draw`, painel e `open`.
3. Observa o livro ausente e as contagens `11 total / 10 visible / 1 hidden`.
4. Roda `history` e vê somente o snapshot por metadados.
5. Remove a linha `hidden: true`, roda `draw` e `open` e vê o livro retornar ao
   mesmo lugar.

A fixture automatizada cobre “Quem mais mora aqui” caso a estante real não
tenha um autor frequente adequado.

- **Observação esperada:** esconder e mostrar são reversíveis, gratuitos e não
  apagam o livro nem seus metadados.
- **Passa:** livro visual some/volta; contagens e história batem; nenhuma rede.
- **Falha:** livro permanece como capa/lombada, autor escondido continua sendo
  contado, ordem muda, dado some do YAML ou qualquer chamada paga acontece.

## Product Principles Preserved

- **A última palavra é de quem lê:** `hidden` decide a página.
- **Nada se perde:** esconder preserva fonte, posição e histórico.
- **Desenhar é grátis:** a correção usa somente `check`/`draw`/`open`.
- **Terminal como protótipo:** operação pura explicita o futuro botão sem
  investir em novo comando descartável.

## Risks and Ambiguities

- Um título escondido pode continuar citado na lente ou no texto. Isso é
  deliberado: remover prosa automaticamente violaria a autoria da pessoa.
- Uma prateleira vazia continua visível. Decidir ocultá-la ou movê-la pertence
  à organização da DS3, não a esta correção.
- Índices são suficientes para a operação interna v1; IDs estáveis só serão
  necessários quando uma interface concorrente exigir.

## Stop Conditions

- Esconder exigir mudança do formato v1.
- O escopo começar a corrigir títulos/capas ou mover livros.
- A implementação tentar reescrever prosa automaticamente.
- Surgir necessidade de um comando terminal específico.
- A validação pedir comparação de históricos reais sem consentimento.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: Navigator (Alisson)
- Approved on: 2026-10-28
