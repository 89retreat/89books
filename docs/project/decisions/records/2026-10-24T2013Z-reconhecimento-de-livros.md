---
status: Decided
raised: 2026-10-24
decided: 2026-10-25
deciders:
  - Navigator (Alisson)
supersedes:
related:
  - CV1.DS1.TS1
---

# Como reconhecer livros em fotos e prints

## Question

Qual modelo de visão usar para reconhecer lombadas numa foto de estante e
capas num print do Kindle, e qual custo e tempo por foto são aceitáveis?

## Decision

Usar **Claude Sonnet 5.5** (via OpenRouter, só provedores sem retenção para
treino) para reconhecer livros em prints do Kindle e fotos de estante na CV1,
com revisão obrigatória pela pessoa antes de a estante ficar visível. Cada
livro é ligado a uma obra da Open Library; a estante não depende de capa.

## Rationale

Spike CV1.DS1.TS1 ([relatório](../../../../spikes/reconhecimento/relatorio.md)):
Kindle 100% de cobertura com Sonnet 5.5 e Haiku 5.5; estante 88% com Sonnet
contra 60% com Haiku, cujos extras incluíam erros reais de leitura. Custo do
Sonnet: cerca de US$ 0,02 por imagem. Open Library acha a obra de ~72% dos
livros e tem capa para ~60% delas.

## Options Considered

- Claude Sonnet 5.5 para tudo (escolhida).
- Claude Haiku 5.5 para tudo: 10 vezes mais barato, mas fraco em lombadas.
- Haiku para prints e Sonnet para fotos: economia irrelevante no dogfood.

## Consequences

- CV1.DS2.US2 (revisão do reconhecimento) é obrigatória.
- A entrada pede fotos por prateleira, de perto, mais uma foto geral para a
  capa, e reconhece em segundo plano.
- A DS3 precisa de visual próprio para livros sem capa. A segunda fonte de
  metadados (Google Books) ficou para medir antes da DS2.US1; ver
  [stack e hospedagem](2026-10-26T1332Z-stack-e-hospedagem.md).

## Review Trigger

Volume de uso que torne o custo relevante, ou nova geração de modelos.
