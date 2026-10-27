[< Story](index.md)

# Plan — CV1.DS3.US2

## Objective

Fechar o caminho do clone à estante: um guia em inglês, a pasta
`my-bookshelf/` pronta no clone, fotos do iPhone aceitas e o terminal
indicando o próximo passo do começo ao fim.

## Pull

Puxada em 2026-10-27, logo após a implementação da US1. Fecha a DS3; o
Navigator valida as duas juntas num clone limpo, com as próprias fotos.

## Prepare

- A US1 deixou `my-bookshelf/` inteira ignorada pelo git, o que impede a
  pasta de existir no clone. A regra passa a `my-bookshelf/*` com uma exceção
  para um `README.md` dentro dela.
- Fotos do iPhone vêm em HEIC por padrão. `pillow-heif` (licença BSD, com
  rodas prontas para macOS, Linux e Windows) registra o formato no Pillow;
  conferido em 2026-10-27, versão 1.8.1. O resto do pipeline (rotação,
  redução, sem EXIF) já trata qualquer imagem que o Pillow abra.
- Hoje, com a pasta vazia, a configuração da US1 pediria as chaves antes de
  descobrir que não há fotos.

## Scope

- **`GETTING_STARTED.md`** na raiz, em inglês, ligado no topo do README:
  1. o que você precisa: `git`, `uv` (com o comando de instalação),
     uma conta no
     OpenRouter com algum crédito; custo e tempo por estante;
  2. clonar e entrar na pasta;
  3. fotografar: dicas curtas (uma prateleira por foto, de frente, com luz,
     lombadas legíveis; HEIC do iPhone serve) e copiar para `my-bookshelf/`;
  4. `uv run shelf` e o que ele vai perguntar;
  5. abrir `my-bookshelf/shelf.html` e compartilhar o arquivo (WhatsApp ou
     AirDrop, abrir no navegador);
  6. problemas comuns: chave recusada, sem crédito, nenhuma foto encontrada,
     gerar de novo (`--setup`, custo de uma nova rodada).
- **`my-bookshelf/README.md`** versionado: o que pôr ali e o aviso de que
  nada dessa pasta vai para o git.
- **`.gitignore`:** `my-bookshelf/*` e `!my-bookshelf/README.md`.
- **HEIC:** dependência `pillow-heif`, registrada em `photos`; `.heic` e
  `.heif` entram nas extensões aceitas.
- **Mensagens do terminal:**
  - pasta sem fotos: verificada antes da configuração, com a mensagem
    "Put photos of your shelf in my-bookshelf/ (.jpg, .heic, .png...) and run
    `uv run shelf` again";
  - no fim: o caminho de `shelf.html`, "Open it in your browser" com o
    comando para o sistema, e uma linha sobre compartilhar o arquivo.
- README: a seção "Generate your shelf" passa a apontar para o guia.

## Non-Goals

- Instalar `git` ou `uv`, ou checar a versão do Python.
- Converter outros formatos (RAW, vídeo, PDF).
- Abrir o navegador automaticamente.

## Acceptance Behavior

Ver o [índice da story](index.md).

## Validation Route

- Automático: `uv run pytest`, `uv run ruff check . && uv run ruff format --check .`.
  Testes novos: uma foto HEIC é lida, reduzida e sem EXIF; a pasta vazia é
  avisada antes de qualquer pergunta; a mensagem final traz o caminho da
  estante; `git check-ignore` ignora fotos e `config.toml` em `my-bookshelf/`
  e não ignora o `README.md` da pasta.
- Driver: seguir o `GETTING_STARTED.md` ao pé da letra num clone limpo em
  `/tmp`, com uma foto HEIC entre as do Lula, e anotar qualquer passo que o
  guia não explique.
- Navigator, para a DS3 inteira: clonar o repositório numa pasta nova da
  própria máquina, seguir só o guia, pôr as próprias fotos e gerar a estante.
  - Passa: chega à estante sem pedir ajuda nem editar arquivos, e o `git
    status` continua limpo.
  - Falha: um passo do guia que não funciona ou não está escrito, uma foto do
    iPhone recusada, ou um arquivo pessoal no `git status`.

E2E decision: ponta a ponta automatizado com rede simulada; o clone limpo do
Driver e o do Navigator são a rota real.

## Implementation Contract

- TDD em `photos`, `config` e no `main`.
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
