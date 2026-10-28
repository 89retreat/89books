[< Story](index.md)

# Plan — CV2.DS1.US2 Know where my shelf stands

## Pull

Puxada em 2026-10-28 depois do fechamento da US1. Criar, desenhar e abrir já
funcionam, mas a pessoa ainda precisa lembrar os verbos e informar a pasta em
contextos que poderiam ser reconhecidos. A US2 torna a entrada gratuita e
orientadora antes de a US3 acrescentar versões e restauração.

## Prepare

### Estado atual

- `uv run shelf` já não gasta, mas `_show_next` olha apenas a existência de
  `shelf.yaml`, `shelf.html` e `books.yaml`; não lê o contrato, não mostra
  contagens ou datas e não distingue página desatualizada de pronta.
- `draw` já chama `parse_shelf` e mostra erros com linha, mas não existe o
  verbo `check`.
- `shelf.yaml` contém todos os livros, inclusive `hidden`; `history/` ainda
  não é escrito, mas o painel pode contar zero ou versões que já estejam lá
  sem abri-las ou compará-las.
- O default atual é sempre o caminho relativo `my-bookshelf/`. Na validação da
  US1, o Navigator perguntou se omitir `--folder` deveria usar a própria pasta.

### Decisão proposta para a pasta

Sem `--folder`, resolver nesta ordem:

1. **pasta atual**, quando contém `shelf.yaml`, `books.yaml`, `config.toml` ou
   ao menos uma foto suportada;
2. **`my-bookshelf/` dentro da pasta atual**, preservando o fluxo do clone;
3. se nenhum dos dois existe, usar `my-bookshelf/` como destino sugerido para
   começar.

`--folder` sempre vence. Isso permite `shelf` instalado e executado dentro da
própria estante, sem quebrar `uv run shelf` a partir da raiz do repositório.
Nos testes de desenvolvimento fora do projeto, `uv run --project <repo> shelf`
continua sendo necessário; isso é do `uv`, não do produto.

### Fronteira núcleo/terminal

- O terminal coleta fatos do filesystem: caminhos existentes, texto, mtimes,
  quantidade de fotos e arquivos de histórico.
- Um núcleo puro recebe esses fatos e devolve o estado, contagens e a ação
  recomendada. Assim, uma aplicação web pode mostrar o mesmo estado sem
  reproduzir regras do CLI.
- O terminal apenas formata o painel e os horários em inglês.

## Scope

### Núcleo

- Novo módulo puro **`shelf.status`**:
  - `ShelfFacts`: texto e mtime do `shelf.yaml`, mtime da página, quantidade
    de fotos e versões;
  - `ShelfStatus`: estado, livros totais/visíveis/escondidos, erros, stale e
    próximo verbo;
  - `inspect(facts) -> ShelfStatus`, chamando exclusivamente `parse_shelf`.
- Estados e recomendações:
  - `not_created` → `create`;
  - `invalid` → `check`;
  - `not_drawn` → `draw`;
  - `stale` (`shelf.yaml` mais novo que `shelf.html`) → `draw`;
  - `ready` → `open`.
- Nenhum acesso a arquivo, ambiente, relógio, terminal ou rede no módulo.

### Cliente de terminal

- Coletar `ShelfFacts` sem carregar configuração ou chave.
- Painel compacto, por exemplo:

  ```text
  Shelf: /caminho/my-bookshelf
  Photos: 1
  Source: shelf.yaml — 11 books (11 visible) — edited 2026-10-28 17:32
  Page: shelf.html — drawn 2026-10-28 17:34 — up to date
  Versions: 0
  Next: uv run shelf open
  ```

- Em arquivo inválido, mostrar quantidade de erros no painel, sem despejar a
  lista inteira; `Next` aponta para `check`.
- Novo `check`: ausência do arquivo é erro claro; válido imprime livros e
  prateleiras; inválido imprime cada `ShelfYamlIssue` e sai com código 2.
  Nunca escreve nem abre página.
- `_resolve_folder(explicit, cwd)` com a ordem proposta acima; todas as ações
  (`create`, `draw`, `open`, `setup`, `check` e sem verbo) usam a mesma pasta.
- Horários locais estáveis no formato `YYYY-MM-DD HH:MM`; sem linguagem
  relativa como “há dois minutos”, que complica testes e fuso de servidor.
- O painel conta `history/*.yaml`, mas não lê nem compara versões.

### Documentação

- `README.md`, `GETTING_STARTED.md`, `my-bookshelf/README.md`, `--help` e guia
  de desenvolvimento: incluir `check`, o painel e a resolução de pasta.

## Non-Goals

- Executar o próximo comando automaticamente ou perguntar “quer continuar?”.
- Guardar, listar em detalhe, comparar ou restaurar versões (US3).
- Validar existência de capas locais, rede, catálogos ou conteúdo semântico dos
  textos; `check` é o contrato v1 existente.
- Mudar `create`, `draw` ou o formato v1.
- Descobrir estantes fora da pasta atual ou manter um cadastro global.

## Implementation Approach

1. Testes de `status.inspect` para os cinco estados, contagens e múltiplos
   erros; provar ausência de I/O por teste de arquitetura.
2. Testes do resolvedor de pasta: explícita, pasta atual reconhecida, fallback
   `my-bookshelf/` e destino ainda inexistente.
3. Substituir `_show_next` pelo coletor de fatos + painel, com serviços pagos
   injetados que falham se tocados.
4. Adicionar `check` ao parser e ao `main`, sempre chamando `parse_shelf`.
5. Testes de bytes antes/depois para painel e `check`, válidos e inválidos.
6. Atualizar guias e executar E2E gratuito na pasta descartável da US1.

## Test Strategy

```bash
uv run pytest tests/test_status.py tests/test_main.py tests/test_shelf_file.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Casos obrigatórios:

- sem verbo e `check` não leem ambiente, não rodam setup e não chamam criação,
  desenho, abertura ou serviço;
- painel sem arquivo mostra fotos e `create`;
- painel inválido mostra número de erros e `check`;
- painel válido sem página mostra livros, datas, versões e `draw`;
- fonte mais nova mostra `stale` e `draw`; página atualizada mostra `ready` e
  `open`;
- `hidden: true` aparece como total, escondido e não visível;
- `check` válido sai 0; vários erros saem 2 e todos têm linha/caminho;
- painel e `check` preservam bytes e mtimes de `shelf.yaml` e `shelf.html`;
- pasta explícita vence; pasta atual reconhecida vence o fallback; raiz do
  clone ainda escolhe `my-bookshelf/`;
- `history/` inexistente conta zero; somente `*.yaml` é contado.

## Validation Route

Usar `/tmp/estante-alisson-validacao-us1`, sem qualquer chave no ambiente:

1. rodar `uv run shelf --folder /tmp/estante-alisson-validacao-us1` e conferir
   estado pronto, 1 foto, 11 livros, datas e zero versões;
2. rodar `check` e ver o resumo válido;
3. tocar ou editar `shelf.yaml`, abrir o painel e ver `stale` + `draw`;
4. colocar dois erros no arquivo, rodar painel (resumo) e `check` (duas linhas),
   confirmando que a página ainda abre;
5. restaurar o arquivo e desenhar novamente;
6. numa pasta de teste dentro do checkout, entrar nela e comprovar que omitir
   `--folder` usa a pasta atual; da raiz, comprovar o fallback `my-bookshelf/`.

- **Observação esperada:** o painel sempre explica estado e próximo verbo;
  `check` detalha erros; nenhuma ação pede chave, confirmação ou custo.
- **Passa:** estados, contagens, datas e recomendação correspondem aos arquivos;
  resolução de pasta é previsível; bytes permanecem intactos.
- **Falha:** gasto ou setup, pasta surpreendente, estado/recomendação errados,
  erro sem linha, ou qualquer arquivo alterado.

## Acceptance Behavior

Ver o [índice da story](index.md).

## Product Principles Preserved

- **Gastar é sempre uma escolha:** entrar sem verbo e conferir nunca chegam a
  setup ou serviço pago.
- **Nada se perde:** painel e check são estritamente somente leitura.
- **A última palavra é de quem lê:** o estado nasce do `shelf.yaml` atual, não
  de cache ou inferência que substitua o arquivo.

## Risks and Ambiguities

- A resolução inteligente de pasta é mais conveniente, mas adiciona uma regra
  implícita. O painel sempre imprime o caminho escolhido na primeira linha e
  `--folder` continua sendo a saída explícita.
- Mtime é suficiente para “editado depois de desenhado”, mas não prova
  igualdade de conteúdo. Hash e snapshots pertencem à US3, que guarda versões.
- A contagem de versões antecipa somente a leitura do diretório; a experiência
  de histórico continua integralmente na US3.

## Stop Conditions

- O painel precisar abrir configuração, ambiente ou rede.
- A pasta atual puder vencer um `--folder` explícito.
- `check` duplicar regras de validação fora de `parse_shelf`.
- Detectar stale exigir mudar o formato v1 ou escrever metadados.
- O escopo começar a guardar ou restaurar versões.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: pending
- Approved on: pending
