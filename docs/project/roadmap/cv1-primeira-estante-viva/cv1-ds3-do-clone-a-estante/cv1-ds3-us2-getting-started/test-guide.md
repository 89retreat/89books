[< Story](index.md)

# Test Guide — CV1.DS3.US2

## Automated Validation

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Testes novos: uma foto HEIC é lida, reduzida e sem EXIF; `.heic` e `.heif`
são listadas; a pasta vazia é avisada antes de qualquer pergunta; a mensagem
final diz onde está a estante e como compartilhá-la; o git ignora fotos,
`config.toml`, a estante gerada e o cache em `my-bookshelf/`, mas não o
`README.md` da pasta.

## E2E Decision

Ponta a ponta automatizado com rede simulada; o Driver seguiu o guia num
clone limpo, e a validação do Navigator é a rota real da DS3.

## Navigator Validation (DS3 inteira, com a US1)

1. Clone o repositório numa pasta nova da sua máquina, seguindo só o
   `GETTING_STARTED.md`.
2. Ponha as suas fotos em `my-bookshelf/` e rode `uv run shelf`.
3. Abra a estante e confira o `git status`.

Passa: chega à estante sem pedir ajuda nem editar arquivos, e o `git status`
continua limpo. Falha: um passo do guia que não funciona ou não está escrito,
uma foto do iPhone recusada, ou um arquivo pessoal no `git status`.

## Validation Evidence

2026-10-27, Driver, seguindo o guia num clone limpo em `/tmp`:

- `uv run pytest`: 85 testes passando. `ruff` limpo.
- O clone já trazia `my-bookshelf/` só com o `README.md`. Com a pasta vazia,
  `uv run shelf` disse para pôr as fotos, sem perguntar nada.
- Seis fotos do Lula em JPEG e uma convertida para HEIC (`IMG_0009.HEIC`).
  Com elas dentro, `git status` continuou limpo.
- O assistente da US1 pediu nome e chaves, testou e gravou; anunciou US$ 0,17
  e o gasto foi US$ 0,18. 156 livros, 25 deles vindos da foto HEIC.
- No fim: "Your shelf is ready: my-bookshelf/shelf.html", o comando para
  abrir e como compartilhar.
- Depois da geração, `git status` limpo; a página sem chaves nem caminhos
  locais. O clone foi apagado.
- Não exercitado pelo Driver: o clone pelo GitHub com o convite, a instalação
  do `uv` numa máquina nova e a criação de conta no OpenRouter. Ficam para a
  validação do Navigator.
