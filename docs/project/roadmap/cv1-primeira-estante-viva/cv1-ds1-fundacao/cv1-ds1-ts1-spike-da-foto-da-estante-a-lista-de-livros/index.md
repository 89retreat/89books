---
code: CV1.DS1.TS1
level: Technical Story
status: Planned
status_reason:
updated: 2026-10-25
related:
  - ../../../../decisions/records/2026-10-24T2013Z-reconhecimento-de-livros.md
---

[< Parent](../index.md)

# CV1.DS1.TS1 — Spike: da foto da estante à lista de livros

**Status:** Planned
**Type:** Technical Story

---

## Technical Story

In order to decidir como a entrada da CV1 reconhece livros,
As o time que vai construir a DS2,
I want to medir um pipeline automático de foto ou print até uma lista de obras na Open Library,
So that a escolha de modelo, custo e forma da entrada se apoie em números reais e não em impressão.

## Outcome

Um relatório com números por tipo de imagem (print do Kindle e foto de
prateleira) e uma recomendação, que fecha o registro de decisão
"reconhecimento de livros".

## Acceptance Behavior

```text
Given os prints do Kindle do Raphael e as fotos de prateleira do Lula, com gabaritos revisados pelos donos
When o script do spike roda sobre cada imagem
Then cada imagem produz uma lista de livros ligados a obras da Open Library, com capa quando houver
And o relatório mostra, por tipo de imagem: livros do gabarito encontrados, livros inventados, livros achados na Open Library, duplicados removidos, custo e tempo por imagem
And o registro "reconhecimento de livros" passa para Decided com a abordagem recomendada
And nenhuma imagem ou lista pessoal entra no git
```

## Scope

- Script descartável em `spikes/reconhecimento/`.
- Extração por modelo de visão (título, autor, status de leitura quando houver).
- Busca e normalização na Open Library, ligando cada livro à obra (*work*),
  não à edição.
- Remoção de duplicados entre imagens da mesma pessoa.
- Comparação de pelo menos dois modelos.
- Relatório `spikes/reconhecimento/relatorio.md` com números agregados, sem
  listas pessoais.

## Out Of Scope

- Interface de upload, revisão ou estante (DS2 e DS3).
- Banco de dados e código de produção.
- Fotos de visão geral (07 e 08 do Lula): servem como capa, não entram na
  medição.
- Afinidade entre estantes. A interseção encontrada fica só como observação.

## Validation

Automatizada: o script roda sobre todas as amostras e gera o relatório.
Navigator: ler o relatório e decidir a abordagem da entrada; os gabaritos
foram revisados por Raphael e Lula antes da medição final.
