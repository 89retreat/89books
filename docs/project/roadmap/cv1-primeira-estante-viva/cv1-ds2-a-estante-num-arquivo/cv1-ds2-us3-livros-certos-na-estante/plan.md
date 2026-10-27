[< Story](index.md)

# Plan — CV1.DS2.US3

## Objective

Conferir título e autoria de cada livro antes de montar a página, mostrar o
autor nas lombadas e dar à prateleira das sobras um lugar mais leve, com um
título que diga que são livros que um dia me chamaram a atenção.

## Pull

Puxada em 2026-10-27, a partir do feedback do Lula sobre a estante gerada na
US2. O Navigator escolheu, entre os caminhos propostos: conferência pelo
modelo, Google Books como segunda fonte, autor na lombada e a prateleira das
sobras com cara de rodapé e título fixo.

## Prepare

- A US3 original ("Corrigir a estante e pedir outro retrato") vira a
  CV1.DS2.US4. A correção automática vem antes da manual: o que o sistema
  pode conferir sozinho não deve chegar à pessoa como tarefa.
- O spike `spikes/reconhecimento/segunda_fonte.py` já consulta o Google Books.
  A cota anônima respondeu 429 na primeira consulta (2026-10-26), por isso a
  chave é necessária.
- A conferência reaproveita `openrouter.complete` e a lista numerada já usada
  pelo retrato.
- Os débitos adiados da US2 se cruzam com esta story: a geração real final
  também exercita o descarte de capas escaneadas e o layout final.

## Scope

- **Conferência pelo modelo** (novo módulo `review`): uma chamada só de
  texto, depois da Open Library e do Google Books, com a lista numerada
  (título lido, autor lido, título e autor encontrados, quando houver). O
  modelo devolve, por livro: título corrigido, autores, e se é duplicata de
  outro número ou se não é livro. Ele só corrige quando tiver segurança e usa
  o contexto da estante inteira. A leitura da resposta descarta números
  inválidos e nunca apaga um livro sem marcar o motivo. Custo esperado: US$
  0,01 a 0,02 por estante.
- **Google Books** (novo módulo `googlebooks`): consultado para os livros que
  a Open Library não achou ou achou sem autor. Chave em `GOOGLE_BOOKS_API_KEY`
  ou `google_books_api_key` no `config.toml`. Sem chave, a etapa é pulada com
  um aviso, e o resto da geração segue. Cache em `.shelf/googlebooks.json`.
  Capas do Google Books entram só se a Open Library não tiver capa, passando
  pelo mesmo filtro de miolo escaneado.
- **Ordem da geração:** reconhecer → deduplicar → Open Library → Google Books
  → conferência → nova busca na Open Library para os títulos corrigidos (com
  cache) → capas → retrato.
- **Autor na lombada:** o sobrenome do primeiro autor, menor, embaixo do
  título, dentro da mesma lombada. A espessura passa a considerar título e
  sobrenome.
- **Prateleira das sobras:** sem numeral, fundo mais leve, sempre na largura
  toda e no fim da página. Título fixo, proposto: "Livros que um dia me
  chamaram a atenção", sem parágrafo. O Navigator pode trocar o texto ao
  aprovar o plano.
- `books.yaml` passa a registrar, por livro, se o título foi corrigido e por
  qual fonte, para a US4 e para a pessoa entenderem de onde veio cada dado.
- README: a chave do Google Books e o que a conferência faz.

## Non-Goals

- Ler as fotos em faixas.
- Editar o `books.yaml` à mão, cache do reconhecimento e `--new-portrait`
  (US4).
- Testes automáticos do layout no navegador (débito adiado da US2).

## Acceptance Behavior

```text
Given uma estante em que o modelo leu "Continuo Preto", sem autor
When gero a estante
Then o livro aparece como "Continuo Preta", de Sueli Carneiro
And um nome de autor lido como título é corrigido ou vira autoria de um livro
And o mesmo livro lido duas vezes aparece uma vez só
```

```text
Given um livro com autor conhecido
When ele aparece como lombada
Then a lombada mostra o sobrenome do autor, menor, embaixo do título
```

```text
Given livros que não entraram em nenhum tema
When abro a estante
Then eles aparecem no fim, numa prateleira sem numeral e mais leve,
     com o título "Livros que um dia me chamaram a atenção"
```

```text
Given nenhuma chave do Google Books
When gero a estante
Then a geração termina, avisa que pulou o Google Books e faz a conferência pelo modelo
```

## Validation Route

- Automático: `uv run pytest` e `uv run ruff check . && uv run ruff format --check .`.
  Testes novos cobrem a leitura da conferência (correções, duplicatas, não
  livros, números inválidos), o cliente do Google Books com rede simulada e
  sem chave, a ordem da geração, o sobrenome na lombada e a prateleira das
  sobras.
- Driver: gerar de novo a estante do Lula numa pasta fora do repositório,
  com as duas chaves (cerca de US$ 0,12), e conferir no `books.yaml` e no
  navegador: "Continuo Preta — Sueli Carneiro", "Carla Akotirene" resolvido,
  "O Pai Prezado" sem duplicata, autores nas lombadas, a prateleira das
  sobras e as capas escaneadas ainda descartadas. Medir quantos livros
  ganharam autor e quantos títulos mudaram.
- Navigator, com o Lula: abrir a estante nova e dizer se os livros estão
  certos.
  - Passa: o Lula reconhece os títulos e autores e não se incomoda com a
    última prateleira.
  - Falha: um livro certo virou errado na conferência, livros sumiram sem
    motivo, ou a última prateleira ainda soa como sobra.

E2E decision: ponta a ponta automatizado com rede simulada; a geração real é
a rota do Driver e do Navigator.

## Dependency

- Chave gratuita da Books API (Google Cloud), criada pelo Navigator e posta em
  `GOOGLE_BOOKS_API_KEY`. Sem ela, a story pode ser implementada e testada,
  mas a validação real fica sem a segunda fonte.

## Implementation Contract

- TDD em `review`, `googlebooks`, `shelves` e no pipeline.
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
- pending confirmation: `navigator_approval`
