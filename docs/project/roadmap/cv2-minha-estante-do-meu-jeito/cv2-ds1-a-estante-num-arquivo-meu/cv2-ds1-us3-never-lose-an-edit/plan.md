[< Story](index.md)

# Plan — CV2.DS1.US3 Never lose an edit

## Pull

Puxada em 2026-10-28 depois do fechamento da US2. A pessoa já sabe criar,
conferir, desenhar e entender o estado da estante. Falta cumprir a última
promessa da DS1: qualquer comando que substitua `shelf.yaml` preserva antes o
que estava ali, e uma edição desenhada vira um ponto recuperável.

## Prepare

### Estado atual

- `draw_shelf` valida e renderiza tudo em memória antes de substituir
  `shelf.html`, mas não registra o conteúdo desenhado.
- `create_shelf` recusa substituição; não existem `recreate`, `history` ou
  `restore`.
- O painel conta arquivos YAML em `history/`, porém ainda não distingue
  versões gerenciadas de arquivos estranhos.
- `shelf.yaml` e `shelf.html` já usam escrita temporária e substituição
  atômica no cliente.
- O núcleo não lê pastas, relógio, terminal ou ambiente. Essa fronteira deve
  continuar válida para histórico e restauração.

### Invariantes de segurança

1. **Snapshot exato:** guardar os bytes de `shelf.yaml`, sem parsear e
   serializar novamente; comentários, estilo e até uma edição inválida são
   preservados.
2. **Validar antes de substituir:** a versão escolhida por `restore` precisa
   passar em `parse_shelf` antes de qualquer mutação.
3. **Backup antes da troca:** `restore` e `recreate` escrevem a versão atual
   com sucesso antes da substituição atômica de `shelf.yaml`.
4. **Falha mantém a fonte:** falha de geração, validação, snapshot ou escrita
   nunca substitui `shelf.yaml`.
5. **Sem comparação implícita:** `history` lista somente metadados; não abre,
   resume ou compara o conteúdo de versões. Ler uma versão acontece apenas
   quando a pessoa a nomeia em `restore`.
6. **Pagamento explícito:** em terminal interativo, `recreate` pergunta; em
   terminal não interativo, `create` e `recreate` recusam gastar sem `--yes`.

## Scope

### Planejamento puro de histórico

Novo módulo **`shelf.history`**, sem acesso a filesystem, relógio atual,
terminal ou ambiente:

- `HistoryEntry(name, modified_at)` para metadados fornecidos pelo cliente;
- `plan_snapshot(entries, now, limit=20)` devolve nome collision-safe e quais
  versões gerenciadas remover depois da nova cópia;
- nomes: `shelf-YYYY-MM-DD-HHMM.yaml`; colisões no mesmo minuto recebem
  `-02`, `-03` etc.;
- reconhecer apenas nomes gerenciados; arquivos alheios nunca entram na
  retenção;
- ordenar e manter as 20 versões gerenciadas mais recentes.

O núcleo recebe tempo e metadados. Não chama `datetime.now()`, não escolhe
pastas e não grava arquivos.

### Adaptador local de armazenamento

No cliente, operações pequenas e testáveis:

- listar entradas gerenciadas em `history/` sem ler seu conteúdo;
- salvar texto exato com criação atômica e modo UTF-8;
- podar somente entradas gerenciadas indicadas pelo plano;
- substituir `shelf.yaml` atomicamente;
- rejeitar nomes com barras, `..`, caminhos absolutos ou que não tenham sido
  listados por `history`;
- usar relógio local injetável nos testes.

### Changed since last draw

- Guardar em `.shelf/last-drawn.sha256` o SHA-256 dos bytes do `shelf.yaml`
  que produziram a página.
- `draw` continua validando, preparando imagens e renderizando primeiro.
- Se o hash atual difere do marcador — ou o marcador ainda não existe —,
  salvar a fonte atual em `history/` antes de substituir a página.
- Depois da página escrita, atualizar o marcador atomicamente.
- Repetir `draw` com os mesmos bytes não cria versão.
- O painel usa o hash quando disponível para decidir `stale`; conserva mtime
  como fallback para estantes anteriores à US3.

### Commands

#### `draw`

- Retorna e mostra o caminho da versão quando uma foi criada.
- Em YAML inválido, não cria versão nem muda página ou marcador.
- Se o snapshot funciona e a página falha, a versão extra é segura; uma nova
  tentativa não perde dados.

#### `history`

- Lista versões gerenciadas da mais nova para a mais antiga: nome, data e
  tamanho; não lê conteúdo.
- Sem versões, explica que o próximo `draw` depois de uma mudança criará uma.
- Sai 0 e nunca altera nada.

#### `restore VERSION`

1. Resolver somente um nome exato impresso por `history`.
2. Ler e validar a versão escolhida.
3. Ler os bytes atuais, mesmo se inválidos.
4. Guardar os bytes atuais em uma nova versão.
5. Substituir `shelf.yaml` atomicamente pelos bytes escolhidos.
6. Não desenhar automaticamente; mostrar `draw` como próximo gesto.

Se versão e fonte atual forem byte a byte iguais, informar que nada mudou e
não criar snapshot.

#### `recreate`

- Exige `shelf.yaml` existente e fotos; ignora `books.yaml` e executa a criação
  completa a partir das fotos.
- Mostra a mesma estimativa da criação completa e confirma antes de qualquer
  chamada paga; `--yes` é consentimento explícito.
- Gera e serializa o novo arquivo inteiramente em memória.
- Somente depois do sucesso, salva os bytes atuais e substitui a fonte
  atomicamente.
- Não desenha automaticamente; a página anterior fica intacta e o painel
  recomenda `draw`.
- Falha paga ou local preserva fonte, página e histórico anterior; se o backup
  já foi criado antes de uma falha de replace, ele permanece como proteção.

### Retention and privacy

- Depois de cada novo snapshot, manter 20 versões gerenciadas.
- Nunca apagar arquivo desconhecido em `history/`.
- Adicionar `**/history/shelf-*.yaml` ao `.gitignore` e cobrir pastas de
  estante fora de `my-bookshelf/`.
- O HTML, histórico e saída não contêm chave, caminho de foto embutido ou
  EXIF novo.

### Documentation

Atualizar `GETTING_STARTED.md`, `README.md`, `my-bookshelf/README.md`, help e
tabela de comandos da CV2 com custo, mutação e exemplos de `history` e
`restore`.

## Non-Goals

- Comparar, resumir ou mostrar diferenças entre versões.
- Restaurar por posição ambígua como “a terceira”; o nome listado é o ID.
- Guardar versões de `shelf.html`, fotos, config ou caches.
- Criar lock multi-process ou transação distribuída; a story cobre um cliente
  local por vez.
- Mudar o formato `shelf.yaml` v1.
- `portrait` isolado, correções de livros ou rearranjo da DS2/DS3.

## Implementation Approach

1. Caracterizar writes atômicos e o fluxo atual de `draw`.
2. TDD do planejador puro: nomes, colisões, ordenação, retenção e arquivos
   desconhecidos.
3. TDD do armazenamento com relógio injetado e falhas em cada fronteira.
4. Integrar snapshot e marcador ao `draw` sem alterar sua renderização.
5. Adicionar `history` e `restore`, incluindo fonte atual inválida e proteção
   contra traversal.
6. Refatorar a construção de `Services` para `create` e `recreate`
   compartilharem geração sem compartilhar política de substituição.
7. Adicionar `recreate`, confirmação paga e exigência de `--yes` no modo não
   interativo para os dois comandos pagos.
8. Atualizar painel, gitignore e documentação.
9. Rodar E2E sintético gratuito; depois validar com a cópia de uma foto e, se
   o Navigator confirmar o custo mostrado, uma única recriação paga.

## Test Strategy

```bash
uv run pytest tests/test_history.py tests/test_cli.py tests/test_main.py tests/test_status.py tests/test_gitignore.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Casos obrigatórios:

- primeiro `draw` após a US3 cria uma versão e marcador; segundo draw idêntico
  não cria outra;
- editar bytes cria nova versão; YAML inválido não cria versão nem muda página
  ou marcador;
- nomes no mesmo minuto não colidem; retenção deixa 20 e ignora arquivos não
  gerenciados;
- `history` não abre arquivos de versão; ordem, data e tamanho são corretos;
- restore rejeita nome ausente, traversal e versão inválida antes de backup ou
  replace;
- restore de fonte atual inválida salva seus bytes exatos e instala uma versão
  válida; página e marcador não mudam;
- falhas de snapshot impedem replace; falha de replace preserva a fonte e o
  snapshot já escrito;
- recreate recusado ou geração falha não cria snapshot; sucesso cria backup
  antes de substituir; nunca desenha;
- paid command não interativo sem `--yes` recusa antes de setup ou serviço;
- nenhuma operação lê ou compara o conteúdo de versões não selecionadas;
- painel usa hash quando presente e conta somente versões gerenciadas;
- históricos de qualquer pasta de estante ficam ignorados pelo git;
- arquitetura rejeita filesystem, relógio atual, ambiente e terminal no
  planejador puro.

## Validation Route

Criar `/tmp/estante-alisson-validacao-us3` como cópia descartável da estante
de uma foto, sem levar chaves para o repositório.

### Free route

1. Confirmar painel pronto e contagem inicial.
2. Alterar uma frase de `lens` e rodar `draw`; observar “Saved version”.
3. Rodar `draw` novamente sem editar; contagem não muda.
4. Rodar `history`; observar lista sem conteúdo ou diff.
5. Quebrar `shelf.yaml` de propósito e restaurar o nome escolhido.
6. Confirmar que o arquivo quebrado também foi guardado, `check` volta a passar
   e a página anterior permaneceu até um novo `draw`.

### Paid route — one photo only

1. Rodar `recreate` e primeiro recusar; comprovar zero mutação e zero gasto.
2. Rodar novamente, observar estimativa para uma foto e somente continuar com
   confirmação explícita do Navigator.
3. Depois do sucesso, observar backup, fonte nova, página anterior preservada
   e `draw` recomendado.
4. Restaurar a versão pré-recreate e redesenhar gratuitamente.

Não executar uma estante completa. Não ler, diffar ou resumir o conteúdo das
versões reais sem consentimento adicional.

- **Observação esperada:** cada substituição anuncia o backup; versões podem
  ser listadas e restauradas; nenhuma confirmação recusada muda algo.
- **Passa:** bytes são recuperáveis, limite é 20, página só muda em `draw`,
  gasto acontece uma vez e somente após confirmação.
- **Falha:** edição some, histórico é comparado sem autorização, arquivo
  desconhecido é apagado, versão inválida substitui a fonte, ou serviço pago é
  chamado sem consentimento.

## Product Principles Preserved

- **Nada se perde:** snapshot termina antes da substituição da fonte.
- **Gastar é sempre uma escolha:** confirmação interativa ou `--yes` explícito.
- **A última palavra é de quem lê:** restore devolve bytes escolhidos pela
  pessoa; não funde nem reinterpreta.
- **Terminal como cliente fino:** núcleo planeja; cliente escolhe pasta, relógio
  e escrita.

## Risks and Ambiguities

- O marcador pode falhar depois de página e snapshot; isso pode gerar uma cópia
  extra na tentativa seguinte, nunca perda. Duplicata segura é preferível a
  inferir comparando conteúdos históricos sem consentimento.
- Uma edição inválida pode ser guardada por restore/recreate. Ela é evidência
  recuperável, mas não pode ser restaurada pelo comando até ser corrigida.
- A retenção deliberadamente remove a 21ª versão gerenciada mais antiga; não há
  versões fixadas nesta story.
- Um processo local por vez é a suposição explícita. Concorrência de servidor
  exigirá armazenamento transacional próprio.

## Stop Conditions

- Precisar comparar conteúdo de versões não selecionadas.
- Recreate sobrescrever antes de snapshot concluído.
- Restore aceitar caminho livre em vez de ID listado.
- Planejador puro precisar de `Path`, `datetime.now()`, ambiente ou terminal.
- Teste pago exigir mais que a única foto já separada.
- O escopo migrar para correção, rearranjo ou publicação.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: Navigator (Alisson)
- Approved on: 2026-10-28
