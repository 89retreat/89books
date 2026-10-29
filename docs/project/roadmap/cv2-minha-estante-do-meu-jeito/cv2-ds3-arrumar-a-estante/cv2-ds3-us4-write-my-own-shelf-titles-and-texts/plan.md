[< Story](index.md)

# Plan — CV2.DS3.US4 Write my own shelf titles and texts

## Pull

Puxada pelo Navigator em 2026-10-29, logo após o fechamento de CV2.DS3.US3.
Prateleiras, ordem, frente/lombada e foto principal já pertencem à pessoa;
agora a linguagem que apresenta a estante também precisa ser explicitamente
autoral.

## Prepare

### Estado atual

- `shelf.yaml` v1 já exige `lens`, exige título não vazio em cada seção e
  aceita `text` ausente ou textual.
- Parse e dump já preservam textos multilinha; texto vazio permanece uma
  escolha válida para `lens` e `section.text`.
- `render_file` já usa literalmente `shelf.lens`, `section.title` e
  `section.text`, sem consultar retrato, catálogo ou modelo.
- Jinja escapa HTML em todos os campos. O filtro `emphasize` escapa primeiro e
  converte pares simples `*texto*` em `<em>` somente na abertura e nos textos
  das seções; títulos de seção permanecem texto literal.
- Citações entre asteriscos no texto de uma seção também alimentam a regra
  automática de frente/lombada para livros sem escolha `face` explícita.
- A última seção só recebe semântica de fechamento quando mantém o título
  canônico “E mais livros que já me acompanharam” e não tem texto.
- `draw` já guarda os bytes alterados antes de substituir a página, e
  `restore` recupera bytes exatos; falta caracterizar o fluxo para essas
  edições e oferecer operações puras nomeadas.

### Decisões da fatia

1. **Fonte literal:** `lens`, `title` e `text` chegam à página na ordem e com o
   conteúdo escritos, sujeitos apenas ao escape seguro e ao itálico delimitado
   por asteriscos.
2. **Itálico limitado:** `*trecho*` vale na abertura e no parágrafo de seção.
   Títulos de seção não interpretam markup; seus asteriscos aparecem como
   caracteres normais.
3. **HTML nunca é conteúdo ativo:** `<script>`, tags e entidades escritas pela
   pessoa aparecem como texto, inclusive dentro de `*...*`.
4. **Vazio é escolha:** `lens: ''` omite conteúdo da abertura sem invalidar a
   fonte; `text: ''` ou ausência de `text` remove o parágrafo. O título da
   seção continua obrigatório e não vazio.
5. **Citação recompõe só o automático:** alterar `*título do livro*` pode mudar
   qual capa automática fica de frente naquela seção. `face: true` e
   `face: false` continuam vencendo o texto.
6. **Fechamento é explícito:** escrever texto na seção canônica ou trocar seu
   título a transforma numa seção regular numerada, como definido em US1.
7. **Sem novo comando ou schema:** edição direta, `check`, `draw`, `history`,
   `restore` e `open` continuam a superfície.

## Scope

### Renderer characterization

Provar no renderer de arquivo:

- abertura autoral é mostrada literalmente e aceita `*itálico*`;
- título de seção é literal, escapado e não interpreta asteriscos;
- texto de seção é literal, escapado e aceita `*itálico*`;
- tags HTML não são executadas nem introduzidas no DOM como tags autorais;
- pares de asteriscos não atravessam quebras de linha;
- texto vazio não cria parágrafo de seção;
- seções e livros preservam ordem e metadata;
- texto autoral numa seção vazia continua visível.

### Pure operations

Adicionar ao núcleo:

```python
set_shelf_lens(shelf: ShelfFile, lens: str) -> ShelfFile

rewrite_shelf_section(
    shelf: ShelfFile,
    shelf_index: int,
    *,
    title: str,
    text: str,
) -> ShelfFile
```

Contrato:

- retornam cópias sem mutar a fonte;
- `lens` e `text` exigem strings, mas podem ser vazios;
- `title` exige texto não vazio, como o contrato v1;
- a operação de seção preserva livros, ordem e todos os metadados;
- preservam todos os outros campos e seções;
- índice negativo ou ausente levanta `IndexError`;
- tipo inválido ou título vazio levanta `ValueError`.

### Automatic composition interaction

Caracterizar uma seção com dois livros cobertos:

- citar `*Livro A*` deixa A automaticamente de frente;
- reescrever o texto para citar `*Livro B*` move a face automática para B sem
  reordenar livros;
- `face: false` em A e `face: true` em B continuam soberanos, qualquer que seja
  a citação;
- citação aproximada continua usando o mecanismo de similaridade já existente;
- texto sem citação deixa lombadas, salvo a regra canônica de fechamento.

Não alterar o algoritmo de similaridade nesta story.

### History and free flow

- `check` aceita as edições válidas sem escrever arquivos.
- `draw` incorpora os textos, salva snapshot apenas quando a fonte mudou e não
  chama chave, catálogo, rede ou modelo.
- erro estrutural preserva página, marcador e histórico.
- `history` continua exibindo apenas metadados.
- `restore` recupera os bytes e, depois de um `draw` explícito, a linguagem da
  versão escolhida volta à página.
- Testes usam somente histórico descartável; nenhum histórico real de fundador
  será lido ou comparado.

### Documentation

Documentar em `GETTING_STARTED.md` e `my-bookshelf/README.md`:

```yaml
lens: Eu volto sempre a *Torto Arado*.
shelves:
  - title: Livros que me dão chão
    text: Aqui conversam *Torto Arado* e *Quarto de Despejo*.
```

Explicar:

- asteriscos funcionam em `lens` e `text`, não em `title`;
- HTML aparece como texto seguro;
- `text` vazio remove o parágrafo;
- citações podem mudar faces automáticas, mas nunca escolhas explícitas;
- `check`/`draw` são gratuitos e histórico/restore são a rede de segurança;
- `recreate` é uma reconstrução paga e explícita da fonte inteira: salva a
  edição anterior, mas não é o caminho para redesenhar textos autorais.

## Non-Goals

- Markdown geral, links, listas, negrito, headings ou HTML autorizado.
- Editor rico, preview em tempo real, novo comando CLI ou interface gráfica.
- Mudar fonte, cor, tamanho, layout ou tipografia da página.
- Reescrever nome da pessoa, livros, autores, capas, ordem ou foto principal.
- Novo schema, campos de autoria ou distinção estrutural entre texto gerado e
  texto editado.
- Alterar similaridade de títulos ou a regra de frente/lombada.
- Preservar textos através de `recreate`; ele continua sendo substituição
  explícita e paga, protegida por snapshot.
- Pedir outro retrato por modelo; isso pertence a CV2.DS3.US5, se for puxada.

## Implementation Approach

1. Escrever testes vermelhos para `set_shelf_lens` e
   `rewrite_shelf_section`, cobrindo pureza, validação e preservação.
2. Caracterizar escape e itálico em abertura/texto, além de título literal e
   campos vazios no renderer.
3. Caracterizar a troca de face automática causada pela mudança de citação e
   provar a precedência de `face` explícito.
4. Cobrir `check`/`draw`/snapshot/restore com textos autorais e erros seguros,
   sem alterar o contrato ou os verbos.
5. Atualizar instruções e preparar E2E offline com duas versões de linguagem.
6. Rodar suíte completa e parar no checkpoint de validação do Navigator.

## Test Strategy

```bash
uv run pytest tests/test_core.py tests/test_page.py tests/test_shelves.py tests/test_shelf_file.py tests/test_cli.py tests/test_history.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Casos obrigatórios:

- operações puras não mutam fonte, livros ou seções vizinhas;
- `lens`/`text` vazios são aceitos; tipos inválidos e título vazio são
  rejeitados;
- índices negativos e ausentes são rejeitados;
- abertura e texto mostram conteúdo autoral e itálico;
- título de seção mantém asteriscos literais;
- HTML e scripts são escapados antes do itálico;
- asteriscos sem par ou atravessando newline permanecem texto;
- mudança de citação recompõe apenas faces automáticas e conserva ordem;
- `face` explícito vence qualquer texto;
- escrever na seção canônica remove seu tratamento de fechamento;
- seção sem livros mantém título e texto;
- parse/dump preservam texto multiline e vazio no contrato v1;
- `check` é somente leitura; `draw` salva a fonte alterada e permanece offline;
- erro preserva página, marcador e histórico;
- restore descartável recupera linguagem anterior em bytes exatos;
- núcleo continua sem terminal, ambiente ou filesystem.

## Validation Route

Criar `/tmp/89books-ds3-us4-validation` com uma foto local, duas capas locais e
uma seção com dois livros em ordem:

1. abrir a versão inicial, cuja seção cita `*Livro A*`;
2. editar `lens` para uma frase pessoal com `*Livro B*` e `<minha voz>`;
3. editar o título da seção para `Minha *prateleira* <autoral>`;
4. editar o texto para citar `*Livro B*` e incluir `<script>não executar</script>`;
5. rodar `check`, `draw` e `open` sem chave;
6. confirmar abertura e parágrafo autorais, Livro B em itálico, tags visíveis
   como texto seguro, asteriscos literais no título e face automática em B;
7. pôr `face: false` em B e confirmar que a lombada explícita vence a citação;
8. remover a marca, desenhar de novo e confirmar retorno ao automático;
9. usar `history` e uma versão descartável para restaurar a linguagem anterior,
   redesenhando explicitamente depois do restore.

- **Observação esperada:** a página fala com as palavras exatas da pessoa;
  itálico e face automática respondem às citações, sem executar HTML.
- **Passa:** conteúdo literal e seguro, ordem intacta, precedência de `face`,
  restauração exata e zero chave/rede/custo.
- **Falha:** texto gerado reaparece, HTML executa, título interpreta markup,
  livros reordenam, citação vence `face` explícito, restore perde linguagem ou
  qualquer serviço pago é solicitado.

## Product Principles Preserved

- **A última palavra é de quem lê:** o texto da fonte vence a proposta inicial
  da IA.
- **Cada leitor revela a própria lógica:** a linguagem e os agrupamentos vêm da
  pessoa; citação só orienta o automático onde ela não escolheu `face`.
- **A estante não precisa explicar a pessoa:** é possível reduzir ou apagar
  textos, sem formulário obrigatório nem interpretação adicional.
- **Nada se perde:** snapshots e restore protegem a linguagem anterior.
- **Gastar é escolha:** escrever, conferir, desenhar, abrir e restaurar são
  gratuitos.
- **Terminal como protótipo:** operações puras servem a futuros campos de
  edição sem prender a regra ao CLI.

## Risks and Ambiguities

- Asteriscos cumprem dois papéis: itálico e citação para composição automática.
  A documentação precisa tornar esse efeito visível para não parecer surpresa.
- `lens: ''` mantém o elemento estrutural vazio no HTML; esta story não altera
  layout para removê-lo, apenas preserva a escolha textual permitida pelo v1.
- Texto YAML multiline continua um único parágrafo visual porque o template usa
  `<p>`; suporte a múltiplos parágrafos exigiria outro contrato e fica fora.
- Escrever texto na seção canônica muda seu status visual para seção regular,
  comportamento já decidido em US1 e agora explicitamente caracterizado.
- `recreate` substitui textos por um novo retrato, mas salva a fonte anterior.
  Confundir `draw` gratuito com `recreate` pago é risco de documentação, não
  motivo para ampliar esta story.

## Stop Conditions

- A solução exigir Markdown geral, HTML permitido ou versão nova do schema.
- A story começar a redesenhar tipografia/layout ou o algoritmo de similaridade.
- A implementação tentar inferir se um texto é “humano” ou “gerado”.
- Preservar textos em `recreate` exigir mapear semanticamente seções novas e
  antigas.
- A validação exigir chave, catálogo, modelo, rede ou pagamento.
- A solução precisar ler ou comparar histórico real de fundador.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: pending
- Approved on: pending
