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

<Preenchido depois das rodadas.>
