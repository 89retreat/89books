[< Story](index.md)

# Test Guide — CV1.DS1.TS2

## Automated Validation

- `cd spikes/reconhecimento && uv run pytest`: os testes do spike continuam
  passando depois do novo script `segunda_fonte.py`.
- `grep -l "status: Open" docs/project/decisions/records/*` não lista
  interface principal nem acesso do grupo.

## E2E Decision

Não exigido. A story só produz registros de decisão e documentação.

## Navigator Validation

Ler os registros:

- `docs/project/decisions/records/2026-10-24T2013Z-interface-principal.md`
- `docs/project/decisions/records/2026-10-24T2013Z-acesso-do-grupo.md`
- `docs/project/decisions/records/2026-10-26T1332Z-stack-e-hospedagem.md`

Observação esperada: cada registro com decisão para o MVP local,
justificativa ligada ao relatório da TS1 e à ES-002, e consequências para a
DS2, a DS3 e a CV2.

Passa: o Navigator reconhece a justificativa e aceita as três decisões.
Falha: decisão sem justificativa, em conflito com os princípios ou com o
relatório, ou que o Navigator não sustenta.

## Validation Evidence

2026-10-26:

- `uv run pytest`: 22 testes passando.
- Os três registros estão `Decided`; o briefing e o guia local foram
  atualizados.
- Google Books não medido: a API anônima respondeu 429 já na primeira
  consulta. O script fica pronto para rodar com chave.
- 2026-10-26: decisões reescritas para o MVP local depois da ES-002; a
  versão com servidor ficou registrada para a CV2.
- Pendente: validação do Navigator.
