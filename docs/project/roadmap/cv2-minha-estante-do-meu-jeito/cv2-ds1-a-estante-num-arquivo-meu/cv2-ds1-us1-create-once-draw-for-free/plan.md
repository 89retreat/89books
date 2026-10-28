[< Story](index.md)

# Plan — CV2.DS1.US1 Create once, draw for free

## Pull

Puxada em 2026-10-28 depois das duas Technical Stories da DS1: o núcleo já
separa geração e desenho do terminal, e `shelf.yaml` v1 já é um contrato
executável. Esta é a primeira fatia que entrega essa separação para a pessoa.

## Prepare

### Estado atual

- `shelf.cli.main` ainda tem um único caminho pago: `shelf [folder]` carrega
  chave, confirma custo, reconhece, desenha e grava `shelf.html` e
  `books.yaml` de uma vez.
- `core.generate` já devolve livros, retrato, custo e nomes de fotos sem gravar
  a estante. `core.draw` ainda recebe o modelo plano da CV1.
- `shelf_file.parse_shelf` e `dump_shelf` já definem `version: 1`, prateleiras
  explícitas, livros em ordem, `cover_photo`, `lens` e proveniência.
- `page.render` ainda organiza prateleiras a partir do retrato. Para desenhar
  do arquivo, a organização precisa acontecer na conversão da geração para
  `ShelfFile`; depois disso, o arquivo é a autoridade.
- Uma pasta CV1 tem `books.yaml` estruturado, fotos, configuração, caches e
  `shelf.html`, mas o retrato só existe renderizado no HTML. Migrar sem reler
  fotos significa reaproveitar os livros e as capas e pagar apenas por um novo
  retrato. Não vamos tentar extrair estrutura do HTML.

### Decisões deste plano

- **`create` e `draw` continuam separados.** `create` grava apenas
  `shelf.yaml`; a pessoa roda `draw` para criar ou substituir a página. Isso
  torna o gasto e a sobrescrita da página explícitos e preserva a página CV1
  até a primeira rodada bem-sucedida de `draw`.
- **Migração automática e barata.** Se existe `books.yaml` e não existe
  `shelf.yaml`, `create` lê os livros salvos, não chama reconhecimento,
  Open Library, Google Books, revisão nem conferência de capas; chama apenas o
  retrato, depois converte para v1. O custo e o tempo menores aparecem antes
  da confirmação. O `books.yaml` antigo não é apagado nem reescrito.
- **A página deriva somente do novo arquivo.** Depois de criado,
  `shelf.yaml` fornece nome, foto de capa, lente, prateleiras, textos, ordem,
  livros, visibilidade, frente/lombada e capa. `config.toml` fornece apenas
  nome e chaves; um `cover_photo` legado é usado uma vez na criação e deixa
  de comandar o desenho.
- **O arquivo congela a primeira composição.** A conversão registra a ordem e
  o `face: true/false` que a página CV1 calculava, para que o primeiro desenho
  não reorganize a estante. As histórias da DS2 e DS3 tornam essas escolhas
  superfícies editáveis e validadas pela pessoa.
- **Setup vira verbo.** A troca de parser já necessária nesta story move o
  comportamento atual de `--setup` para `shelf setup`; não acrescenta regra
  de produto, apenas preserva a configuração guiada sob o vocabulário
  decidido para a CV2.
- **Sem verbo, sem gasto.** Antes do painel completo da US2, `uv run shelf`
  mostra uma orientação mínima baseada somente na existência de
  `shelf.yaml`/`shelf.html`. O uso antigo sem verbo deixa de gerar.

## Scope

### Núcleo

- **`core.create(...) -> CreatedShelf`**: operação que recebe fotos,
  configurações, serviços e opcionalmente o texto de um `books.yaml` CV1.
  Sem dados antigos, chama `generate`; com eles, valida e reutiliza livros e
  `left_out`, chama só o retrato. Devolve `ShelfFile`, custo e se houve
  migração; nunca grava.
- **Conversão para v1**: usa a composição atual de `build_shelves` para
  congelar prateleiras, ordem e frente/lombada; remove campos de apresentação
  (`spine`, ângulo, posição) e converte `cover_id` em URL, `cover_url` em
  `cover` e ausência de capa em `none` apenas quando necessário preservar uma
  escolha explícita.
- **`core.draw(ShelfFile, images) -> str`**: desenha as prateleiras na ordem do
  arquivo, ignora livros `hidden`, respeita `face` e `cover`, calcula apenas
  propriedades visuais derivadas (lombada, inclinação, numeral e coluna) e não
  chama serviço.
- Leitura pura do legado em `books.py`: texto YAML para livros e `left_out`,
  com erro claro e sem I/O.

### Cliente de terminal

- Parser com `create`, `draw`, `open`, `setup`; opção comum
  `--folder <path>` e `--yes` em `create`.
- `create`:
  1. recusa imediatamente se `shelf.yaml` existir;
  2. confere fotos e setup necessário;
  3. detecta `books.yaml`, mostra estimativa de migração ou geração completa e
     confirma antes da chamada paga;
  4. chama o núcleo e grava `shelf.yaml` atomicamente;
  5. informa custo, quantidade de livros e o próximo comando (`draw`).
- `draw`:
  1. não lê nem exige chave;
  2. lê `shelf.yaml`, mostra todos os `ShelfYamlError` com linha e caminho;
  3. encontra as fotos da pasta e põe `cover_photo` primeiro;
  4. prepara imagens, renderiza tudo em memória e só então substitui
     `shelf.html` atomicamente;
  5. informa que não houve custo e sugere `open`.
- `open`: recusa claramente se a página não existir; caso exista, usa uma
  função injetável sobre `webbrowser.open` e não passa pelo shell.
- `setup`: comportamento atual de configuração guiada, sem chamada paga.
- Sem verbo: mensagem mínima e gratuita. Não implementa as contagens, datas e
  versões da US2.
- O formato posicional antigo (`shelf caminho/`) deixa de ser uma geração
  implícita; os guias mostram somente verbos e `--folder`.

### Documentação

- `README.md`, `GETTING_STARTED.md`, `my-bookshelf/README.md` e bloco de
  comandos do guia de desenvolvimento.
- Explicar que `create` custa e ocorre uma vez; `draw` e `open` são gratuitos;
  pastas CV1 reutilizam `books.yaml`; depois de `shelf.yaml`, o arquivo antigo
  permanece apenas como legado.

## Non-Goals

- Painel detalhado, `check`, datas e contagem de versões (US2).
- Backup, histórico, restore e recreate (US3). Como ainda não há histórico, a
  validação manual usa uma cópia descartável.
- Nova operação de retrato, adição de fotos, publicação ou edição assistida.
- Polimento específico de `hidden`, capas locais, movimentação, textos ou
  foto de capa: o desenho respeita o contrato, mas essas experiências são
  fechadas nas DS2 e DS3.
- Extrair o retrato antigo do HTML da CV1.

## Implementation Approach

1. **Caracterização do CLI:** testes novos fixam que sem verbo não chama build,
   `create` recusa arquivo existente antes de setup/custo e `draw` não precisa
   de chave.
2. **Conversão no núcleo:** testes de `core.create` com serviços falsos para os
   caminhos novo e CV1; no legado, fakes de reconhecimento e catálogos que
   falham se chamados.
3. **Desenho explícito:** separar em `shelves` a transformação de
   `ShelfFile` para dados da página e mudar `page.render` para receber a
   composição pronta. Testes com ordem, `hidden`, `face`, capas e autores
   frequentes visíveis.
4. **Comandos e escrita segura:** funções pequenas para cada verbo, leitura e
   gravação no cliente, `Path.replace` somente depois de validação e render
   completos.
5. **Migração e setup:** parser do `books.yaml` legado, estimativa reduzida e
   configuração que pede somente o necessário para o caminho escolhido.
6. **Docs e compatibilidade:** atualizar instruções; manter os módulos antigos
   apenas onde os testes de geração ainda os exercitam, sem continuar
   produzindo `books.yaml` em criação nova.

## Test Strategy

```bash
uv run pytest tests/test_core.py tests/test_shelf_file.py tests/test_cli.py tests/test_main.py tests/test_page.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Casos obrigatórios:

- criação nova escreve somente `shelf.yaml` e chama o pipeline pago uma vez;
- criação sobre `shelf.yaml` existente não chama setup, confirmação nem
  serviço e não altera bytes;
- migração CV1 chama somente o retrato e preserva livros, capas,
  proveniência, `left_out`, foto escolhida e arquivo legado;
- confirmação recusada deixa a pasta intocada;
- desenho funciona sem variáveis de chave e sem qualquer fake de rede;
- YAML inválido lista todos os erros e mantém os bytes do HTML anterior;
- falha de foto ou render também mantém o HTML anterior;
- desenho válido reflete ordem, lente, textos e livros do arquivo e não muda o
  `shelf.yaml`;
- `open` recebe a URI correta; ausência da página é erro claro;
- comando sem verbo e `--help` não gastam;
- HTML continua sem chave, caminho local ou EXIF.

## Validation Route

### Driver E2E

Usar uma cópia em `/tmp` de uma pasta CV1 com fotos e `books.yaml` já salvos
(preferencialmente `/tmp/estante-lula`, se ainda existir):

1. remover somente `shelf.yaml` da cópia;
2. rodar `uv run shelf create --folder <cópia>` e confirmar a estimativa de
   apenas um retrato;
3. verificar no log e nos caches que nenhuma foto ou catálogo foi relido;
4. rodar `uv run shelf draw --folder <cópia>` sem chaves no ambiente;
5. editar a lente na cópia, desenhar de novo e confirmar mudança instantânea;
6. quebrar o YAML, desenhar e comparar o hash da página anterior;
7. restaurar o YAML, rodar `open` e apagar a cópia ao final.

Nenhuma geração integral paga será repetida: o único gasto novo é o retrato da
migração, estimado em poucos centavos.

### Navigator

Sobre uma cópia descartável de uma estante CV1 própria ou de fundador:

```bash
uv run shelf create --folder <cópia>
uv run shelf draw --folder <cópia>
uv run shelf open --folder <cópia>
```

Depois, alterar uma frase de `lens` no `shelf.yaml`, rodar `draw` novamente e
abrir a página no computador e no celular. Por fim, introduzir um erro simples
no YAML e confirmar que o comando mostra a linha e preserva a página anterior.

- **Observação esperada:** `create` anuncia que reutilizou `books.yaml`, pede
  confirmação só para o retrato e cria o arquivo; `draw` leva segundos, diz
  que foi gratuito e reflete a edição; `open` abre a página; o erro não apaga
  a página válida.
- **Passa:** nenhuma foto é reconhecida novamente, nenhum catálogo é chamado,
  `create` nunca substitui `shelf.yaml`, `draw` não pede chave nem gasta e a
  página no computador/celular corresponde ao arquivo.
- **Falha:** gasto implícito, perda de arquivo ou página, releitura das fotos,
  edição ignorada ou erro sem linha.

## Acceptance Behavior

Ver o [índice da story](index.md).

## Product Principles Preserved

- **A última palavra é de quem lê:** depois de `create`, somente o conteúdo do
  `shelf.yaml` decide a página.
- **Nada se perde:** `create` não substitui o arquivo e `draw` só troca a
  página depois de validar e renderizar com sucesso; o legado fica intacto.
- **Gastar é sempre uma escolha:** só `create` chama serviço, sempre depois de
  custo e confirmação; sem verbo, `draw`, `open` e `setup` nunca gastam.

## Risks and Ambiguities

- A migração escreve um retrato novo porque a CV1 não guardou o antigo como
  dados. O plano escolhe esse pequeno custo em vez de um parser frágil de HTML.
- `create` e `draw` separados exigem dois comandos na primeira vez, mas tornam
  explícito o limite entre geração paga e desenho gratuito.
- A escrita de histórico ainda não existe. Por isso `draw` protege a página,
  mas a validação manual deve acontecer numa cópia até a US3.

## Stop Conditions

- A migração exigir reler fotos ou consultar catálogos.
- Desenhar do arquivo exigir mudar o contrato v1.
- Uma operação paga puder acontecer sem confirmação.
- Uma falha puder substituir `shelf.yaml` ou uma página válida.
- O escopo começar a fechar histórias de edição da DS2/DS3 em vez de apenas
  respeitar o contrato já definido.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: Navigator (Alisson)
- Approved on: 2026-10-28
