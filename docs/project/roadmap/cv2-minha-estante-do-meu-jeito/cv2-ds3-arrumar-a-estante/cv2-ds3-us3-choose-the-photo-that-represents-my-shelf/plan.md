[< Story](index.md)

# Plan — CV2.DS3.US3 Choose the photo that represents my shelf

## Pull

Puxada pelo Navigator em 2026-10-29, depois do fechamento de CV2.DS3.US2. A
ordem, a frente e a lombada já pertencem à pessoa; agora a foto que apresenta
a presença física da estante também precisa ter uma única autoridade editável.

## Prepare

### Estado atual

- `shelf.yaml` v1 já exige `cover_photo` como texto não vazio.
- A criação põe a primeira foto recebida em `cover_photo`; por compatibilidade,
  `load_config` ainda pode mover uma antiga escolha de `config.toml` para a
  primeira posição antes da criação.
- `draw` já procura o nome exato entre as fotos do diretório, põe a escolhida
  primeiro e entrega essa ordem ao mosaico; a primeira célula é a de destaque.
- `draw` já mantém a página anterior quando a foto escolhida não existe.
- `check` valida o YAML e capas de livros locais, mas ainda não verifica se
  `cover_photo` existe entre as fotos da estante.
- `recreate` carrega `config.toml` novamente e pode deixar uma escolha legada
  influenciar a nova fonte, embora `shelf.yaml` já exista.
- O núcleo ainda não oferece uma operação nomeada para escolher a foto nem uma
  regra pura compartilhada para ordenar nomes de fotos.

### Decisões da fatia

1. **Nome exato e arquivo existente:** `cover_photo` referencia uma das fotos
   de estante no nível raiz, com extensão já aceita por `load_photos`.
2. **Fonte única depois da criação:** uma marca antiga de `config.toml` só pode
   orientar a criação inicial; com `shelf.yaml` existente, ela é ignorada.
3. **Recriação preserva a escolha:** `recreate` conserva o `cover_photo` atual
   se o arquivo ainda existe. Se a fonte estiver inválida ou a foto tiver sido
   removida, a reconstrução usa a primeira foto válida e continua sendo uma
   recuperação explícita, com snapshot anterior.
4. **Mesma validação gratuita:** `check` e `draw` resolvem a escolha pela mesma
   função; ambos falham antes de qualquer mutação quando o nome não existe.
5. **Destaque sem reordenar o resto:** a escolhida vai para a primeira célula;
   as demais mantêm a ordem determinística retornada por `load_photos`.
6. **Sem novo comando ou schema:** a pessoa edita uma linha, roda `check`,
   `draw` e `open`; o contrato continua v1.
7. **Configuração legada não é apagada:** `setup` continua preservando campos
   desconhecidos para não destruir dados locais, mas `cover_photo` deixa de
   ter autoridade quando a fonte existe.

## Scope

### Pure operations

Adicionar ao núcleo:

```python
set_cover_photo(shelf: ShelfFile, cover_photo: str) -> ShelfFile
```

Contrato:

- retorna cópia sem mutar a fonte;
- exige texto não vazio;
- preserva nome, lente, seções, livros e `left_out`;
- a existência do arquivo é validada pelo cliente que conhece os ativos.

Adicionar uma regra pura de ordenação de nomes, reutilizável pelo terminal e
por um servidor futuro:

```python
order_shelf_photos(photo_names: list[str], cover_photo: str) -> list[str]
```

Contrato:

- exige que a escolha esteja na lista;
- põe a escolha primeiro;
- preserva a ordem relativa e a cardinalidade das demais;
- não lê pasta, ambiente, configuração nem imagem.

### Shared local validation

- Criar no cliente uma resolução única que combina `load_photos` com
  `order_shelf_photos` e converte escolha ausente em `CommandError` claro.
- Usar essa resolução em `check_shelf` e `draw_shelf`.
- Em erro, `draw` preserva `shelf.html`, `.shelf/last-drawn.sha256` e histórico;
  `check` permanece somente leitura.
- Caminhos, subpastas, arquivos sem extensão aceita e nomes aproximados não
  contam como fotos disponíveis: só igualdade com `Path.name` das fotos
  listadas no nível raiz.

### Configuration and recreation authority

- Manter a migração de `config.toml` para `shelf.yaml` somente quando `create`
  ainda não tem fonte.
- Ignorar `cover_photo` legado ao carregar configuração para uma estante que
  já possui `shelf.yaml`.
- Em `recreate`, ler a escolha atual quando a fonte é válida e reaplicá-la ao
  resultado gerado se ela ainda estiver entre as fotos.
- Se a fonte atual não puder ser lida ou a foto não existir, deixar a
  reconstrução escolher a primeira foto válida; o snapshot exato existente
  continua permitindo retorno.
- Não comparar conteúdo de snapshots de histórico.

### Mosaic characterization

- Provar que a imagem escolhida chega primeiro ao HTML e recebe a primeira
  geometria de `mosaic`.
- Provar que trocar apenas `cover_photo` muda o destaque, sem reler fotos por
  modelo, livros, textos ou ordem das demais fotos.
- Caracterizar desktop e celular; no celular, onde só cinco fotos aparecem, a
  escolhida continua presente por estar primeiro.
- Manter preparo já existente: rotação, redução e remoção de metadata antes da
  incorporação no HTML autocontido.

### Documentation

Documentar em `GETTING_STARTED.md` e `my-bookshelf/README.md`:

```yaml
cover_photo: minha-estante-03.jpg
```

Explicar nome exato, arquivo na pasta da estante, `check` antes de `draw`,
redraw gratuito, a primeira célula em destaque e a compatibilidade legada de
`config.toml` somente na primeira criação.

## Non-Goals

- Upload, cópia, renomeação, remoção ou edição de fotos.
- Crop, enquadramento, zoom, filtros ou uma capa diferente por dispositivo.
- Escolher capa de livro; isso pertence a CV2.DS2.US2.
- Alterar quantidade ou geometria das células do mosaico.
- Novo comando CLI, seletor interativo ou interface gráfica.
- Nova versão do YAML ou `cover_photo` opcional/automático.
- Ler fotos com modelo, consultar catálogo, rede ou serviço pago.
- Apagar automaticamente `cover_photo` de `config.toml`.

## Implementation Approach

1. Escrever testes vermelhos para `set_cover_photo` e
   `order_shelf_photos`, incluindo imutabilidade, ordem e erros.
2. Extrair a resolução local compartilhada e caracterizar `check`/`draw` com
   escolha válida, ausente, subpasta e extensão não aceita.
3. Limitar `config.toml` à migração da criação inicial e testar que uma fonte
   existente vence uma marca legada divergente.
4. Preservar a escolha válida durante `recreate`, com testes para escolha
   existente, foto removida e fonte inválida recuperável.
5. Caracterizar a primeira imagem e a ordem das restantes no HTML, sem mudar
   CSS/JS se o comportamento atual já satisfizer a story.
6. Atualizar instruções e preparar um E2E gratuito com fotos coloridas.
7. Rodar a suíte completa e parar no checkpoint de validação do Navigator.

## Test Strategy

```bash
uv run pytest tests/test_core.py tests/test_config.py tests/test_cli.py tests/test_page.py tests/test_shelves.py tests/test_main.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Casos obrigatórios:

- operação pura troca a foto sem mutar a fonte ou outros campos;
- texto vazio ou não textual é rejeitado;
- ordenação põe a escolhida primeiro e preserva todas as demais;
- escolha ausente é rejeitada com nome claro;
- `check` e `draw` aceitam JPG, PNG, WEBP e HEIC listados no nível raiz;
- `check` e `draw` rejeitam foto removida, caminho/subpasta e extensão não
  aceita pela mesma regra;
- erro não altera página, marcador ou histórico;
- HTML incorpora a escolhida primeiro sem revelar caminho ou metadata;
- no mosaico móvel, a escolha permanece entre as fotos visíveis;
- criação inicial ainda migra `cover_photo` legado;
- com `shelf.yaml` existente, configuração legada divergente é ignorada;
- `recreate` preserva escolha válida da fonte e recupera quando ela some ou a
  fonte está inválida;
- nenhum fluxo gratuito lê chave ou chama serviço de rede/modelo.

## Validation Route

Criar `/tmp/89books-ds3-us3-validation` com seis fotos locais de cores e nomes
visivelmente diferentes, além de uma fonte pequena:

1. definir `cover_photo` para a quarta foto na ordem alfabética;
2. rodar `check`, `draw` e `open` sem chave;
3. confirmar que a quarta foto abre o mosaico na célula grande e que as outras
   conservam sua ordem;
4. abrir numa largura de celular e confirmar que a escolhida continua visível;
5. trocar `cover_photo` para outra foto, repetir `check`/`draw`/`open` e
   confirmar que só o destaque muda;
6. definir temporariamente um nome ausente, rodar `check` e `draw`, confirmar o
   erro e que a página anterior continua abrindo;
7. restaurar uma escolha válida e redesenhar gratuitamente.

- **Observação esperada:** a linha `cover_photo` decide imediatamente qual foto
  representa a estante, em desktop e celular.
- **Passa:** escolha exata em destaque, demais fotos em ordem, erro seguro para
  nome ausente, página anterior preservada e zero chave/rede/custo.
- **Falha:** primeira foto alfabética vence a escolha, `config.toml` interfere,
  foto escolhida some no celular, demais fotos reordenam, erro substitui a
  página ou algum serviço pago é solicitado.

## Product Principles Preserved

- **A foto da estante física é a presença:** a pessoa escolhe qual presença
  abre a visita.
- **A última palavra é de quem lê:** `shelf.yaml` vence ordem de arquivo e
  configuração legada.
- **Nada se perde:** erro não substitui a página; `recreate` mantém snapshot e
  preserva a escolha quando possível.
- **Gastar é escolha:** escolher, conferir, desenhar e abrir são gratuitos.
- **Terminal como protótipo:** operações puras e resolução compartilhada servem
  a um controle futuro sem prender a regra ao CLI.

## Risks and Ambiguities

- Preservar a escolha durante `recreate` é uma exceção deliberada ao restante
  do retrato regenerado: foto principal é uma decisão explícita e independente
  do modelo.
- Uma fonte inválida não oferece escolha confiável para preservar; `recreate`
  continua sendo rota explícita de recuperação e guarda os bytes anteriores.
- `check` passará a exigir que as fotos referenciadas estejam presentes. Isso
  aproxima sua promessa de “pronto para desenhar”, mas testes sintéticos que
  validavam só o YAML precisarão criar a foto mínima.
- O arquivo legado em `config.toml` pode continuar fisicamente presente; o que
  sai é sua autoridade, não a linha local.

## Stop Conditions

- A solução exigir alterar o schema ou tornar `cover_photo` opcional.
- A seleção começar a copiar, editar ou enviar fotos.
- `check` ou `draw` precisar de chave, rede, catálogo, modelo ou pagamento.
- Preservar a escolha em `recreate` exigir comparar snapshots reais.
- A mudança no mosaico exigir redesenho visual além de caracterizar a primeira
  célula já existente.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: Navigator (Alisson)
- Approved on: 2026-10-29
