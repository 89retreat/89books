[< Story](index.md)

# Test Guide — CV2.DS1.US1 Create once, draw for free

## Automated Validation

```bash
uv run pytest tests/test_core.py tests/test_shelf_file.py tests/test_cli.py tests/test_main.py tests/test_page.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Cobrir criação nova, migração da CV1 sem reconhecimento ou catálogos, recusa
de sobrescrita, confirmação de custo, desenho sem chave/rede, proteção da
página em qualquer falha, abertura no navegador e comando sem verbo sem gasto.

## Navigator Validation

Em uma cópia descartável de uma estante CV1:

```bash
uv run shelf create --folder <cópia>
uv run shelf draw --folder <cópia>
uv run shelf open --folder <cópia>
```

Editar uma frase de `lens`, desenhar novamente e abrir no computador e no
celular. Depois introduzir um erro no YAML e confirmar a linha indicada e que
a página anterior continua idêntica.

Passa quando `books.yaml` é reutilizado sem releitura de fotos ou catálogos,
`draw` não pede chave nem gasta, a edição aparece e nenhum erro substitui a
página. Falha com gasto implícito, perda, releitura, edição ignorada ou erro
sem linha.

## Validation Evidence

### Driver — 2026-10-28

- `uv run pytest`: 128 testes passando.
- `uv run ruff check . && uv run ruff format --check .`: limpo.
- Testes com serviços que falham se chamados provam que a migração usa somente
  o retrato; criação sobre arquivo existente não chega a setup, confirmação ou
  serviço; desenho sem chaves não chama rede; erro de YAML, foto ou render
  preserva os bytes da página anterior.
- E2E gratuito com foto sintética e sem chaves: `draw` escreveu a página; YAML
  inválido devolveu linha 3 e o SHA-256 da página ficou idêntico.
- E2E real numa cópia de `/tmp/estante-lula`: 160 livros do `books.yaml`
  viraram 7 prateleiras no `shelf.yaml`; somente `Writing your portrait...`
  apareceu, o custo foi US$ 0,03, os caches e o `books.yaml` mantiveram os
  mesmos hashes, e nenhuma foto ou catálogo foi relido. `draw` funcionou sem
  chaves, uma mudança na lente apareceu na rodada seguinte e o HTML não
  continha caminho local. A cópia foi apagada.
- A estimativa de migração foi ajustada de US$ 0,02 para US$ 0,03 a partir da
  medição real.

### Navigator

Pendente: executar a rota acima numa cópia descartável, abrir no computador e
no celular, editar a lente e confirmar a preservação da página diante de um
erro no YAML.
