[< Story](index.md)

# Test Guide — CV1.DS3.US1

## Automated Validation

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Os testes do `setup` e do `main` usam entrada e rede simuladas: primeira
configuração completa, chave rejeitada e aceita na segunda tentativa, três
recusas sem gravar nada, Google Books pulado e lembrado, `config.toml`
existente preservado, chaves do ambiente não perguntadas, pasta padrão
`my-bookshelf/`, custo recusado sem nenhum gasto, `--yes`, `--setup` e
nenhuma pergunta sem terminal interativo.

## E2E Decision

Ponta a ponta automatizado com entrada e rede simuladas; o Driver passou pelo
assistente real num clone limpo, num pseudo-terminal.

## Navigator Validation

Junto com a US2, na validação da DS3: num clone limpo, com as próprias fotos
em `my-bookshelf/`, rodar `uv run shelf`.

Passa: chega à estante sem editar arquivo nem pedir ajuda, e o custo
anunciado bate com o gasto. Falha: pergunta confusa, chave errada descoberta
só no meio da geração, custo surpresa, ou chave ou foto no `git status`.

## Validation Evidence

2026-10-27, Driver:

- `uv run pytest`: 79 testes passando. `ruff` limpo.
- Clone limpo em `/tmp`, sem as variáveis de ambiente das chaves, com as 7
  fotos do Lula em `my-bookshelf/`, conduzido por um pseudo-terminal:
  - pediu o nome; explicou como obter a chave do OpenRouter e que é preciso
    crédito; recusou uma chave errada antes de ler qualquer foto; aceitou a
    certa e mostrou o saldo (US$ 4,82);
  - explicou a chave do Google Books, aceitou e testou a chave;
  - gravou `my-bookshelf/config.toml` com nome e chaves;
  - anunciou "7 photos, about US$ 0.17, about 6 minutes"; o gasto real foi
    US$ 0,17 (163 livros, 7 corrigidos, 22 confirmados no Google Books, 79
    com capa).
- `git status` limpo depois da geração: a pasta `my-bookshelf/` inteira passou
  a ser ignorada (antes, só a configuração e os arquivos gerados eram, e as
  fotos teriam aparecido).
- Página sem chaves e sem caminhos locais. O clone, que guardava as chaves,
  foi apagado.
- Tropeço do Driver, não do comando: a primeira tentativa de automatizar o
  terminal respondeu antes do prompt, e o `getpass` descarta o que foi
  digitado antes de perguntar. Nada foi gasto.
