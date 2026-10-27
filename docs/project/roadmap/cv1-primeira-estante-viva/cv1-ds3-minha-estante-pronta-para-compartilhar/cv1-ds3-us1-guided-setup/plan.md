[< Story](index.md)

# Plan — CV1.DS3.US1

## Objective

Fazer `uv run shelf` conduzir a pessoa do clone à estante: configurar o que
falta, testar as chaves e avisar o custo antes de gastar, tudo em inglês.

## Pull

Puxada em 2026-10-27, logo após o Navigator reescrever a CV1 como a
capacidade de ir do clone à estante. O Navigator decidiu: pasta
`my-bookshelf/`, superfície do terminal em inglês, estante em português, e o
Navigator testa primeiro.

## Prepare

- Hoje o comando exige a pasta como argumento e falha com uma mensagem quando
  falta a chave. `config.py` já lê `config.toml` da pasta e as variáveis de
  ambiente; `config.toml` já é ignorado pelo git em qualquer pasta.
- As chamadas de rede já são injetadas nos testes; o assistente segue o mesmo
  padrão (entrada, saída e validadores de chave como parâmetros).
- OpenRouter tem endpoints gratuitos para conferir a chave e o saldo
  (`/api/v1/key` e `/api/v1/credits`). O Google Books responde a uma busca
  com a chave.

## Scope

- **CLI:** `folder` passa a ser opcional, com padrão `my-bookshelf` no
  diretório atual. Novas opções: `--setup` (refazer a configuração) e `--yes`
  (pular a confirmação de custo).
- **Novo módulo `setup`:**
  - decide o que falta: chave do OpenRouter, nome, e se a chave do Google
    Books já foi respondida (preenchida ou pulada de propósito);
  - explica, em poucas linhas e com o link, como obter cada chave e que o
    OpenRouter precisa de crédito;
  - pede cada resposta; a chave é lida sem eco (`getpass`);
  - testa a chave do OpenRouter e mostra o saldo; se o saldo não cobrir a
    estante estimada, avisa; chave rejeitada pede de novo, até três vezes;
  - testa a chave do Google Books; vazia significa pular, gravado como
    `google_books = "skip"` para não perguntar de novo;
  - grava `config.toml` na pasta, preservando o que já existir (como
    `cover_photo`).
- **Antes de gastar:** mostra fotos, custo estimado (cerca de US$ 0,015 por
  foto mais US$ 0,05 da conferência e do retrato) e tempo estimado, e pede
  `Continue? [Y/n]`. Sem terminal interativo (pipe, CI), não pergunta nada:
  falha com a mensagem atual se faltar a chave e segue sem confirmação.
- Variáveis de ambiente continuam valendo e têm precedência; com elas, o
  assistente não pergunta a chave.
- README: o fluxo novo em poucas linhas; o guia completo é a US2.

## Non-Goals

- Guia de primeiros passos, HEIC e `my-bookshelf/` versionada com
  `.gitkeep` (US2).
- Instalar `uv` ou o Python pela pessoa.
- Guardar chaves fora da pasta (keychain, arquivo global).

## Acceptance Behavior

Ver o [índice da story](index.md).

## Validation Route

- Automático: `uv run pytest`, `uv run ruff check . && uv run ruff format --check .`.
  Testes do `setup` com entrada simulada: primeira configuração completa,
  chave rejeitada e aceita na segunda tentativa, Google Books pulado e não
  perguntado de novo, `config.toml` existente preservado, nada perguntado
  quando tudo está configurado, confirmação de custo recusada sem nenhuma
  chamada ao modelo, sem terminal interativo, `--yes`.
- Driver: rodar `uv run shelf` num clone limpo em `/tmp`, com uma cópia das
  fotos do Lula em `my-bookshelf/`, passando pelo assistente de verdade
  (chaves reais, saldo real), e conferir `git status` limpo depois.
- Navigator: o mesmo, na própria máquina, com as próprias fotos, junto com a
  US2 na validação da DS3.
  - Passa: chega à estante sem editar arquivo nem pedir ajuda, e o custo
    anunciado bate com o gasto.
  - Falha: pergunta confusa, chave errada descoberta só no meio da geração,
    custo surpresa, ou chave ou foto aparecendo no `git status`.

E2E decision: ponta a ponta automatizado com entrada e rede simuladas; a
rodada real no clone limpo é a rota do Driver.

## Implementation Contract

- TDD em `setup`, `config` e no `main`.
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
