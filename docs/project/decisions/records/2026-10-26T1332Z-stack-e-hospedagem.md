---
status: Decided
raised: 2026-10-26
decided: 2026-10-26
deciders:
  - Navigator (Alisson), por delegação ao Driver em cadência accelerated; aceite na validação da CV1.DS1.TS2
supersedes:
related:
  - CV1.DS1.TS2
  - CV1.DS1.TS3
---

# Stack, hospedagem e metadados da CV1

## Question

Com que linguagem, framework, banco e hospedagem a CV1 é construída, quanto
custa por mês e de onde vêm os metadados dos livros?

## Decision

- **Python + Django**, com páginas renderizadas no servidor e **HTMX** para as
  interações da revisão e da estante. Ferramentas: `uv`, `pytest`, `ruff`.
- **SQLite** num volume persistente. As fotos ficam no mesmo volume,
  redimensionadas no envio.
- **Reconhecimento em segundo plano** por uma fila guardada no próprio banco,
  processada por um worker na mesma máquina. A biblioteca é escolhida na TS3.
- **Fly.io**, uma máquina na região de São Paulo (`gru`) com volume de 1 GB.
  Deploy pelo GitHub Actions a cada push na `main`, depois dos testes.
- **Metadados:** Open Library como fonte principal, ligada à obra. O Google
  Books entra como complemento só se a medição justificar (ver Consequences).
  A estante tem visual próprio para livros sem capa.

## Rationale

- O spike já tem em Python a chamada ao modelo, a busca na Open Library e o
  casamento de títulos; a DS2 reaproveita essa lógica.
- O Django traz, sem montagem, o que a CV1 precisa: migrações, sessões, testes
  e um admin para a lista de membros e para corrigir dados durante o dogfood.
- Páginas no servidor com HTMX bastam para um grupo de ~10 pessoas e evitam
  um segundo projeto de frontend.
- O reconhecimento leva 7 a 16 s de modelo por imagem, mais a busca de
  metadados. Uma máquina sempre ligada processa isso sem os limites de tempo
  de funções serverless.
- SQLite numa máquina só é suficiente para o volume do dogfood e não tem
  serviço de banco para pagar ou manter.
- Região de São Paulo: o grupo está no Brasil e as fotos ficam perto dele.

## Options Considered

- **Python + Django + HTMX no Fly.io** (escolhida).
- **TypeScript full-stack (Next.js ou SvelteKit) na Vercel com Postgres
  gerenciado:** combina com parte dos colaboradores, mas reescreve o spike e
  exige fila externa para o reconhecimento longo.
- **Python + FastAPI:** mais leve, porém sem admin, sessões e migrações
  prontas.
- **Postgres gerenciado:** mais custo e peças móveis sem ganho para ~10
  pessoas. Migrar continua possível pelo ORM.
- **Telegram como armazenamento de fotos:** acopla os dados ao bot.

## Consequences

- **Custo mensal estimado**, a confirmar com a primeira fatura na TS3:
  - hospedagem de uma máquina pequena com 1 GB de volume: poucos dólares por
    mês (estimativa, sem fatura ainda);
  - reconhecimento: cerca de US$ 0,02 por imagem, menos de US$ 2 para o grupo
    inteiro entrar (medido na TS1);
  - Telegram e Open Library: gratuitos;
  - domínio próprio: opcional; o subdomínio do Fly.io basta para a CV1.
- **Segredos** (chave do OpenRouter, token do bot, chave do Django) ficam nos
  segredos do Fly.io e do GitHub, nunca no repositório.
- **Backup:** cópia periódica do banco e das fotos fora do volume. O mecanismo
  é escolhido na TS3; antes de alguém do grupo entrar, um backup precisa ter
  sido restaurado com sucesso pelo menos uma vez.
- **Segunda fonte de metadados não medida.** A API anônima do Google Books
  respondeu 429 já na primeira consulta (2026-10-26). O script
  `spikes/reconhecimento/segunda_fonte.py` mede a cobertura com uma chave
  gratuita (`GOOGLE_BOOKS_API_KEY`). Medir antes de planejar a CV1.DS2.US1. A
  DS3 tem visual para livros sem capa de qualquer forma.
- **Conta do Fly.io:** decidir na TS3 se fica no nome do Alisson ou da org
  89retreat. É uma decisão de pagamento, não técnica.
- Uma máquina só significa indisponibilidade nos deploys e nenhuma
  redundância, o que é aceitável no dogfood.

## Review Trigger

Abertura para além do grupo, volume que pese no SQLite ou em uma máquina, ou
custo mensal acima de US$ 15.
