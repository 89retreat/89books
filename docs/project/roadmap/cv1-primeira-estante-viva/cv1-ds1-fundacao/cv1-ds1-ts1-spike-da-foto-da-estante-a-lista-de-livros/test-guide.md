[< Story](index.md)

# Test Guide — CV1.DS1.TS1

## Automated Validation

```bash
cd spikes/reconhecimento
uv run pytest
```

Cobre a lógica sem rede: normalização de títulos, deduplicação, casamento com
o gabarito e cálculo de métricas.

Rodadas reais (exigem `OPENROUTER_API_KEY` e as amostras locais):

```bash
uv run python reconhecer.py --modelo anthropic/claude-sonnet-5.5
uv run python reconhecer.py --modelo anthropic/claude-haiku-5.5
```

## E2E Decision

Não se aplica: o spike não tem produto. A validação é o relatório.

## Navigator Validation

Ler `spikes/reconhecimento/relatorio.md`.

- **Observação esperada:** métricas por tipo de imagem e por modelo
  (cobertura, invenções, achados na Open Library, com capa, duplicados
  removidos, custo e tempo por imagem), custo total do spike e uma
  recomendação.
- **Passa se:** os números permitem escolher a abordagem da entrada e o
  Navigator aceita a recomendação.
- **Falha se:** faltam métricas, o custo não foi medido ou a recomendação não
  decorre dos números.

## Validation Evidence

2026-10-25, prompt `v1`, gasto total US$ 0,25.

- `uv run pytest`: 22 testes passando.
- Rodadas completas com Sonnet 5.5 e Haiku 5.5 sobre 3 prints e 7 fotos de
  prateleira; resultados locais em `spikes/reconhecimento/resultados/`.
- Relatório: [spikes/reconhecimento/relatorio.md](../../../../../../spikes/reconhecimento/relatorio.md).
- Cobertura: Kindle 100% nos dois modelos; estante 88% (Sonnet) contra 60%
  (Haiku).
- Pendente: revisão dos gabaritos por Raphael e Lula; validação do
  Navigator.
